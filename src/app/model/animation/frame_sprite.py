from enum import IntEnum

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsItem

from .frame_sprite_item import FrameSpriteItem, ItemEvent


class FrameSpriteColumn(IntEnum):
    """Column indexes for the internal properties as viewed from the model"""

    Name = 0
    Hide = 1
    Lock = 2
    X = 3
    Y = 4
    Alpha = 5
    Hflip = 6
    Vflip = 7
    Zindex = 8


class FrameSprite(QObject):
    """A sprite part of a frame"""

    sigInternalDataChanged = pyqtSignal(int, FrameSpriteColumn)

    def __init__(
        self,
        name: str,
        pix: QPixmap,
        x: int = 0,
        y: int = 0,
        vflip: bool = False,
        hflip: bool = False,
        alpha: int = 0,
    ):
        super().__init__()

        self._pixmap: QPixmap = pix
        self.item = FrameSpriteItem(self._pixmap)
        self.item.subscribe(ItemEvent.zChanged, self.onItemZchanged)
        self.item.subscribe(ItemEvent.posChanged, self.onPosChanged)

        self._name: str = name
        self._x: int = x
        self._y: int = y
        self._vflip: bool = vflip
        self._hflip: bool = hflip
        self._transparency: int = alpha
        self._zIndex: int = 0

        self._hide: bool = False
        self.item.setVisible(not self._hide)

        self._lock: bool = False

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def hide(self) -> bool:
        return self._hide

    @hide.setter
    def hide(self, value: bool):
        self._hide = value
        self.item.setVisible(not value)

    @property
    def lock(self) -> bool:
        return self._lock

    @lock.setter
    def lock(self, value: bool):
        self._lock = value
        self.item.setFlag(QGraphicsItem.ItemIsMovable, not value)
        self.item.setFlag(QGraphicsItem.ItemIsSelectable, not value)

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int):
        self._x = value
        self.item.setX(value)

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: int):
        self._y = value

    @property
    def alpha(self) -> int:
        return self._transparency

    @alpha.setter
    def alpha(self, value: int):
        self._transparency = value

    @property
    def hflip(self) -> bool:
        return self._hflip

    @hflip.setter
    def hflip(self, value: bool):
        self._hflip = value

    @property
    def vflip(self) -> bool:
        return self._vflip

    @vflip.setter
    def vflip(self, value: bool):
        self._vflip = value

    @property
    def zIndex(self) -> int:
        return self._zIndex

    @zIndex.setter
    def zIndex(self, value: int):
        self._zIndex = value
        self.item.setZValue(value)

    def copy(self):
        item = FrameSprite(
            self.name,
            self._pixmap,
            self.x,
            self.y,
            self.vflip,
            self.hflip,
            self.alpha,
        )
        item.zIndex = self.zIndex
        item.hide = False
        item.lock = False
        item.name += "_copy"
        return item

    def onItemZchanged(self, value: int) -> None:
        # The frame instance has knowledge of all the frame--sprites
        # so it has to deal with reordering the items based on it's zvalue

        pass

    def onPosChanged(self, x: int, y: int) -> None:
        self._x = x
        self.sigInternalDataChanged.emit(self._zIndex, FrameSpriteColumn.X)
