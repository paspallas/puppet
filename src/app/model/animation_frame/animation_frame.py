import typing
from . import operation


from PyQt5.QtCore import QObject, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsItem

from ...collection import SpriteStack
from .frame_sprite import FrameSprite


class AnimationFrame(QObject):
    """A Collection of framesprites that compose an animation frame"""

    sigFrameDataChanged = pyqtSignal(int, int)
    sigFrameLayoutAboutToChange = pyqtSignal()
    sigFrameLayoutChanged = pyqtSignal()
    sigAddedItem = pyqtSignal()
    sigAddToScene = pyqtSignal(QGraphicsItem)
    sigDeleteFromScene = pyqtSignal(QGraphicsItem)
    sigSelectedItem = pyqtSignal(int)

    def __init__(self) -> None:
        super().__init__()
        self._sprites = SpriteStack()

    def add(self, sprite: FrameSprite) -> None:
        self._sprites.push(sprite)
        self.bound(sprite)
        self.sigAddedItem.emit()

    def fromPixmap(self, pixmap: QPixmap) -> None:
        sprite = FrameSprite("New", pixmap)
        self.add(sprite)

    def delete(self, model_index: int) -> None:
        sprite = self._sprites.pop(model_index)
        sprite.delete()
        self.unbound(sprite)

    def copy(self, model_index_dst: int, model_index_src: int) -> None:
        sprite = self._sprites[model_index_src]
        copy = sprite.copy()
        self._sprites.insert(model_index_dst, copy)
        self.bound(copy)
        self.sigAddedItem.emit()

    def select(self, model_index: int) -> None:
        self._sprites[model_index].select()

    def get(self, model_index: int, attr: int) -> typing.Any:
        return self._sprites[model_index].get(attr)

    def set(self, model_index: int, attr: int, value: typing.Any) -> None:
        self._sprites[model_index].set(attr, value)

    def moveUp(self, model_index: int) -> None:
        self._sprites.inc(model_index)

    def moveDown(self, model_index: int) -> None:
        self._sprites.dec(model_index)

    def moveTo(self, model_index_dst: int, model_index_src: int) -> None:
        self._sprites.move(model_index_src, model_index_dst)

    def count(self) -> int:
        return FrameSprite.count()

    def bound(self, sprite: FrameSprite) -> None:
        sprite.sigInternalDataChanged.connect(self.spriteDataChanged)
        sprite.sigAddToScene.connect(self.addGraphicItem, type=Qt.DirectConnection)
        sprite.sigDelFromScene.connect(self.removeGraphicItem, type=Qt.DirectConnection)
        sprite.sigIncreaseZ.connect(self.onIncreaseZ, type=Qt.DirectConnection)
        sprite.sigDecreaseZ.connect(self.onDecreaseZ, type=Qt.DirectConnection)
        sprite.sigHint.connect(
            lambda selected: operation.HighLightSelected.apply(self._sprites, selected)
        )
        sprite.sigDeHint.connect(
            lambda: operation.HighLightSelected.revert(self._sprites)
        )

        sprite.connected()

    def unbound(self, sprite: FrameSprite) -> None:
        sprite.sigInternalDataChanged.disconnect()
        sprite.sigAddToScene.disconnect()
        sprite.sigDelFromScene.disconnect()
        sprite.sigIncreaseZ.disconnect()
        sprite.sigDecreaseZ.disconnect()

    @pyqtSlot(int)
    def onIncreaseZ(self, sprite_index: int) -> None:
        if sprite_index == self._sprites.last():
            return

        self.sigFrameLayoutAboutToChange.emit()
        self._sprites.spriteUp(sprite_index)
        self.sigFrameLayoutChanged.emit()
        self.sigSelectedItem.emit(self._sprites.modelIndex(sprite_index + 1))

    @pyqtSlot(int)
    def onDecreaseZ(self, sprite_index: int) -> None:
        if sprite_index == 0:
            return

        self.sigFrameLayoutAboutToChange.emit()
        self._sprites.spriteDown(sprite_index)
        self.sigFrameLayoutChanged.emit()
        self.sigSelectedItem.emit(self._sprites.modelIndex(sprite_index - 1))

    def __len__(self) -> int:
        return len(self._sprites)

    @pyqtSlot(list)
    def spriteDataChanged(self, indexes: typing.List[typing.Tuple[int, int]]) -> None:
        for sprite_index in indexes:
            self.sigFrameDataChanged.emit(
                self._sprites.modelIndex(sprite_index[0]), sprite_index[1]
            )

    @pyqtSlot(QGraphicsItem)
    def addGraphicItem(self, item: QGraphicsItem) -> None:
        self.sigAddToScene.emit(item)

    @pyqtSlot(QGraphicsItem)
    def removeGraphicItem(self, item: QGraphicsItem) -> None:
        self.sigDeleteFromScene.emit(item)
