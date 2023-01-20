from typing import Any

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from ...util.reflection import PropertyList
from .frame_sprite import FrameSprite


class AnimationFrame(QObject):
    """A Collection of framesprites that compose an animation frame"""

    sigFrameDataChanged = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.sprites: list[FrameSprite] = []
        self._property = PropertyList(FrameSprite)

    def add(self, framesprite: FrameSprite) -> None:
        framesprite.sigInternalDataChanged.connect(self.dataChanged)

        framesprite.zIndex = len(self)
        self.sprites.insert(0, framesprite)

    def delete(self, item_index: int) -> None:
        self.sprites.pop(item_index)
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
