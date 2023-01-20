from typing import Any, overload

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap

from ...util.reflection import PropertyList
from .frame_sprite import FrameSprite
from .frame_sprite_item import FrameSpriteItem


class AnimationFrame(QObject):
    """A Collection of framesprites that compose an animation frame"""

    sigFrameDataChanged = pyqtSignal()
    sigAddToScene = pyqtSignal(FrameSpriteItem)
    sigDeleteFromScene = pyqtSignal(FrameSpriteItem)
    sigAddedItem = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.sprites: list[FrameSprite] = []
        self._property = PropertyList(FrameSprite)

    def add(self, framesprite: FrameSprite) -> None:
        framesprite.sigInternalDataChanged.connect(self.dataChanged)
        framesprite.zIndex = len(self)

        self.sprites.insert(0, framesprite)

        self.sigAddToScene.emit(framesprite.item)

    def fromPixmap(self, pixmap: QPixmap) -> None:
        framesprite = FrameSprite("test", pixmap)
        framesprite.sigInternalDataChanged.connect(self.dataChanged)
        framesprite.zIndex = len(self)

        self.sprites.insert(0, framesprite)

        self.sigAddedItem.emit()
        self.sigAddToScene.emit(framesprite.item)

    def delete(self, item_index: int) -> None:
        item = self.sprites.pop(item_index)
        self.sigDeleteFromScene.emit(item.item)

        self.recalcZindexes()

    def copy(self, dst: int, src: int) -> None:
        item = self.sprites[src]
        self.sprites.insert(dst, item.copy())
        self.recalcZindexes()

    def get(self, item_index: int, attr_index: int) -> Any:
        return getattr(self.sprites[item_index], self._property[attr_index])

    def set(self, item_index: int, attr_index: int, value: Any) -> None:
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
        for i, item in enumerate(reversed(self.sprites)):
            item.zIndex = i

    def __len__(self) -> int:
        return len(self.sprites)

    @pyqtSlot()
    def dataChanged(self) -> None:
        self.sigFrameDataChanged.emit()
