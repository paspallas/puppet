import typing

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap

from ...util.reflection import PropertyList
from .frame_sprite import FrameSprite, FrameSpriteColumn
from .frame_sprite_item import FrameSpriteItem


class AnimationFrame(QObject):
    """A Collection of framesprites that compose an animation frame"""

    sigFrameDataChanged = pyqtSignal(int, int)
    sigAddedItem = pyqtSignal()

    sigAddToScene = pyqtSignal(FrameSpriteItem)
    sigDeleteFromScene = pyqtSignal(FrameSpriteItem)

    def __init__(self):
        super().__init__()

        self.sprites: list[FrameSprite] = []
        self._property = PropertyList(FrameSprite)

    def add(self, framesprite: FrameSprite) -> None:
        """Add a new item to the top of the scene"""

        self.sprites.insert(0, framesprite)

        # Set the higher zindex
        framesprite.zIndex = len(self) - 1

        framesprite.sigInternalDataChanged.connect(self.dataChanged)
        self.sigAddToScene.emit(framesprite.item)

    def fromPixmap(self, pixmap: QPixmap) -> None:
        framesprite = FrameSprite("test", pixmap)
        self.sprites.insert(0, framesprite)
        framesprite.sigInternalDataChanged.connect(self.dataChanged)
        framesprite.zIndex = len(self) - 1

        self.sigAddedItem.emit()
        self.sigAddToScene.emit(framesprite.item)

    def delete(self, item_index: int) -> None:
        item = self.sprites.pop(item_index)
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

    def get(self, item_index: int, attr_index: int) -> typing.Any:
        return getattr(self.sprites[item_index], self._property[attr_index])

    def set(self, item_index: int, attr_index: int, value: typing.Any) -> None:
        setattr(self.sprites[item_index], self._property[attr_index], value)

    def count(self) -> int:
        return self._property.count()

    def moveup(self, item_index: int) -> None:
        """Raise the zindex of an item"""

        item = self.sprites.pop(item_index)
        self.sprites.insert(item_index - 1, item)
        self.recalcZindexes()

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
            item.zIndex = i

    def __len__(self) -> int:
        return len(self.sprites)

    @pyqtSlot(list)
    def dataChanged(self, indexes: typing.List[typing.Tuple[int, int]]) -> None:
        for index in indexes:
            self.sigFrameDataChanged.emit(len(self) - index[0] - 1, index[1])
