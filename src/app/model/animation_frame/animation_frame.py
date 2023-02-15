import typing
from . import operation


from PyQt5.QtCore import QObject, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsItem

from .frame_sprite import FrameSprite


class AnimationFrame(QObject):
    """A Collection of framesprites that compose an animation frame"""

    # to models
    sigFrameDataChanged = pyqtSignal(int, int)
    sigFrameLayoutAboutToChange = pyqtSignal()
    sigFrameLayoutChanged = pyqtSignal()
    sigAddedItem = pyqtSignal()

    # to widgets
    sigAddToScene = pyqtSignal(QGraphicsItem)
    sigDeleteFromScene = pyqtSignal(QGraphicsItem)
    sigSelectedItem = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.sprites: list[FrameSprite] = []

    def add(self, sprite: FrameSprite) -> None:
        self.bound(sprite)
        self.sprites.insert(0, framesprite)
        sprite.z = len(self) - 1
        sprite.ready()

        self.sigAddedItem.emit()

    def fromPixmap(self, pixmap: QPixmap) -> None:
        sprite = FrameSprite("New", pixmap)
        self.sprites.insert(0, sprite)
        sprite.z = len(self) - 1

        self.bound(sprite)

        self.sigAddedItem.emit()

    def delete(self, index: int) -> None:
        sprite = self.sprites.pop(index)
        sprite.delete()
        self.unbound(sprite)

        self.recalcZindexes()

    def copy(self, dst: int, src: int) -> None:
        sprite = self.sprites[src]
        copy = sprite.copy()
        self.sprites.insert(dst, copy)
        self.recalcZindexes()

        self.bound(copy)

        self.sigAddedItem.emit()

    def select(self, index: int) -> None:
        self.sprites[item].select()

    def get(self, index: int, attr: int) -> typing.Any:
        return self.sprites[item].get(attr)

    def set(self, index: int, attr: int, value: typing.Any) -> None:
        self.sprites[item].set(attr, value)

    def count(self) -> int:
        return FrameSprite.count()

    def bound(self, sprite: FrameSprite) -> None:
        sprite.sigInternalDataChanged.connect(self.dataChanged)
        sprite.sigAddToScene.connect(self.addGraphicItem, type=Qt.DirectConnection)
        sprite.sigDelFromScene.connect(self.removeGraphicItem, type=Qt.DirectConnection)
        sprite.sigIncreaseZ.connect(self.onIncreaseZ, type=Qt.DirectConnection)
        sprite.sigDecreaseZ.connect(self.onDecreaseZ, type=Qt.DirectConnection)
        sprite.sigHint.connect(
            lambda selected: operation.HighLightSelected.apply(
                self.sprites, self.itemIndex(selected)
            )
        )
        sprite.sigDeHint.connect(
            lambda: operation.HighLightSelected.revert(self.sprites)
        )

        sprite.connected()

    def unbound(self, sprite: FrameSprite) -> None:
        sprite.sigInternalDataChanged.disconnect()
        sprite.sigAddToScene.disconnect()
        sprite.sigDelFromScene.disconnect()
        sprite.sigIncreaseZ.disconnect()
        sprite.sigDecreaseZ.disconnect()

    def itemIndex(self, z: int) -> int:
        return len(self) - z - 1

    @pyqtSlot(int)
    def onIncreaseZ(self, z: int) -> None:
        if z + 1 > len(self) - 1:
            return

        self.sigFrameLayoutAboutToChange.emit()
        index = self.itemIndex(z)
        self.moveup(index)
        sprite = self.sprites[index - 1]
        self.sigFrameLayoutChanged.emit()

        self.sigSelectedItem.emit(self.itemIndex(sprite.z))

    @pyqtSlot(int)
    def onDecreaseZ(self, z: int) -> None:
        if z - 1 < 0:
            return

        self.sigFrameLayoutAboutToChange.emit()
        index = self.itemIndex(z)
        self.movedown(index)
        sprite = self.sprites[index + 1]
        self.sigFrameLayoutChanged.emit()

        self.sigSelectedItem.emit(self.itemIndex(sprite.z))

    @pyqtSlot(int)
    def moveup(self, index: int) -> None:
        """Raise the zindex of an item"""

        item = self.sprites.pop(index)
        self.sprites.insert(index - 1, item)
        self.recalcZindexes()

    @pyqtSlot(int)
    def movedown(self, index: int) -> None:
        """Lower the zindex of an item"""

        item = self.sprites.pop(index)
        self.sprites.insert(index + 1, item)
        self.recalcZindexes()

    def moveTo(self, dst: int, src: int) -> None:
        """Move the item to a specific position in the z-order list"""

        item = self.sprites.pop(src)
        self.sprites.insert(dst, item)
        self.recalcZindexes()

    def recalcZindexes(self) -> None:
        """Z indexes are reversed from the item position in the list"""
        for i, item in enumerate(reversed(self.sprites)):
            item.z = i

    def __len__(self) -> int:
        return len(self.sprites)

    @pyqtSlot(list)
    def dataChanged(self, indexes: typing.List[typing.Tuple[int, int]]) -> None:
        for index in indexes:
            self.sigFrameDataChanged.emit(self.itemIndex(index[0]), index[1])

    @pyqtSlot(QGraphicsItem)
    def addGraphicItem(self, item: QGraphicsItem) -> None:
        self.sigAddToScene.emit(item)

    @pyqtSlot(QGraphicsItem)
    def removeGraphicItem(self, item: QGraphicsItem) -> None:
        self.sigDeleteFromScene.emit(item)
