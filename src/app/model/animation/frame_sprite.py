import typing
from enum import IntEnum

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsItem

from .frame_sprite_item import FrameSpriteItem, ItemEvent
from ...util.image import Image


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

    sigInternalDataChanged = pyqtSignal(list)

    def __init__(
        self,
        name: str,
        pix: QPixmap,
        x: float = 0,
        y: float = 0,
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
        self._x: float = x
        self._y: float = y
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
        if self._hide != value:
            self._hide = value
            self.item.setVisible(not value)

    @property
    def lock(self) -> bool:
        return self._lock

    @lock.setter
    def lock(self, value: bool):
        if self._lock != value:
            self._lock = value
            self.item.setFlag(QGraphicsItem.ItemIsMovable, not value)
            self.item.setFlag(QGraphicsItem.ItemIsSelectable, not value)

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float):
        self._x = value
        self.item.setX(value)

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float):
        self._y = value
        self.item.setY(value)

    @property
    def alpha(self) -> int:
        return self._transparency

    @alpha.setter
    def alpha(self, value: int):
        if self._transparency != value:
            self._transparency = value
            self.item.setPixmap(Image.setAlpha(value, self._pixmap))

    @property
    def hflip(self) -> bool:
        return self._hflip

    @hflip.setter
    def hflip(self, value: bool):
        if self._hflip != value:
            Image.flipHorizontal(self.item)
        self._hflip = value

    @property
    def vflip(self) -> bool:
        return self._vflip

    @vflip.setter
    def vflip(self, value: bool):
        if self._vflip != value:
            Image.flipVertical(self.item)
        self._vflip = value

    @property
    def zIndex(self) -> int:
        return self._zIndex

    @zIndex.setter
    def zIndex(self, value: int):
        if self._zIndex != value:
            self._zIndex = value
            self.item.setZValue(value)

    def copy(self):
        item = FrameSprite(
            self._name,
            self._pixmap,
            self._x,
            self._y,
            self._vflip,
            self._hflip,
            self._alpha,
        )
        item.hide = False
        item.lock = False
        item.name += "_copy"

        return item

    def onItemZchanged(self, value: int) -> None:
        # The frame instance has knowledge of all the frame--sprites
        # so it has to deal with reordering the items based on it's zvalue

        pass

    def onPosChanged(self, x: float, y: float) -> None:
        self._x = x
        self._y = y

        self.sigInternalDataChanged.emit(
            [(self._zIndex, FrameSpriteColumn.X), (self._zIndex, FrameSpriteColumn.Y)]
        )
