import typing

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsItem

from .frame_sprite import FrameSprite
from .frame_sprite_item import FrameSpriteItem


class AnimationFrame(QObject):
    """A Collection of framesprites that compose an animation frame"""

    sigFrameDataChanged = pyqtSignal(int, int)
    sigFrameLayoutAboutToChange = pyqtSignal()
    sigFrameLayoutChanged = pyqtSignal()
    sigAddedItem = pyqtSignal()

    sigAddToScene = pyqtSignal(QGraphicsItem)
    sigDeleteFromScene = pyqtSignal(QGraphicsItem)
    sigSelectedItem = pyqtSignal(QGraphicsItem)

    def __init__(self):
        super().__init__()

        self.sprites: list[FrameSprite] = []

    def add(self, framesprite: FrameSprite) -> None:
        """Add a new item to the top of the scene"""

        self.sprites.insert(0, framesprite)

        # Set the higher zindex
        framesprite.z = len(self) - 1

        framesprite.sigInternalDataChanged.connect(self.dataChanged)
        self.sigAddToScene.emit(framesprite.item)
        framesprite.item.addedToScene()

    def fromPixmap(self, pixmap: QPixmap) -> None:
        framesprite = FrameSprite("test", pixmap)
        self.sprites.insert(0, framesprite)

        framesprite.sigInternalDataChanged.connect(self.dataChanged)
        framesprite.sigIncreaseZ.connect(self.onIncreaseZ)
        framesprite.sigDecreaseZ.connect(self.onDecreaseZ)
        framesprite.z = len(self) - 1

        self.sigAddedItem.emit()
        self.sigAddToScene.emit(framesprite.item)
        framesprite.item.addedToScene()

    def delete(self, item_index: int) -> None:
        item = self.sprites.pop(item_index)
        item.item.aboutToBeRemoved()
        self.sigDeleteFromScene.emit(item.item)

        self.recalcZindexes()

    def copy(self, dst: int, src: int) -> None:
        framesprite = self.sprites[src]
        copy = framesprite.copy()
        copy.sigInternalDataChanged.connect(self.dataChanged)
        self.sprites.insert(dst, copy)
        self.recalcZindexes()

        self.sigAddedItem.emit()
        self.sigAddToScene.emit(copy.item)
        copy.item.addedToScene()

    def select(self, item_index: int) -> None:
        self.sprites[item_index].select()

    def get(self, item_index: int, attr_index: int) -> typing.Any:
        return self.sprites[item_index].get(attr_index)

    def set(self, item_index: int, attr_index: int, value: typing.Any) -> None:
        self.sprites[item_index].set(attr_index, value)

    def count(self) -> int:
        return FrameSprite.count()

    @pyqtSlot(int)
    def onIncreaseZ(self, z: int) -> None:
        if z + 1 > len(self) - 1:
            return

        self.sigFrameLayoutAboutToChange.emit()

        item_index = len(self) - 1 - z
        self.moveup(item_index)
        sprite = self.sprites[item_index - 1]

        self.sigFrameLayoutChanged.emit()
        self.sigSelectedItem.emit(sprite.item)

    @pyqtSlot(int)
    def onDecreaseZ(self, z: int) -> None:
        if z - 1 < 0:
            return

        self.sigFrameLayoutAboutToChange.emit()

        item_index = len(self) - 1 - z
        self.movedown(item_index)
        sprite = self.sprites[item_index + 1]

        self.sigFrameLayoutChanged.emit()
        self.sigSelectedItem.emit(sprite.item)

    @pyqtSlot(int)
    def moveup(self, item_index: int) -> None:
        """Raise the zindex of an item"""

        item = self.sprites.pop(item_index)
        self.sprites.insert(item_index - 1, item)
        self.recalcZindexes()

    @pyqtSlot(int)
    def movedown(self, item_index: int) -> None:
        """Lower the zindex of an item"""

        item = self.sprites.pop(item_index)
        self.sprites.insert(item_index + 1, item)
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
            self.sigFrameDataChanged.emit(len(self) - index[0] - 1, index[1])
