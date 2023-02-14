import typing
from enum import IntEnum

from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPixmapItem

from ...util.image import Image
from .frame_sprite_item import FrameSpriteItem, ItemEvent


class Index(IntEnum):
    """Column indexes for the internal properties as viewed from the QAbstractItemModel"""

    Name = 0
    Hide = 1
    Lock = 2
    X = 3
    Y = 4
    Alpha = 5
    Hflip = 6
    Vflip = 7
    Z = 8


class FrameSprite(QObject):
    """A sprite part of a frame"""

    sigAddToScene = pyqtSignal(QGraphicsItem)
    sigDelFromScene = pyqtSignal(QGraphicsItem)
    sigInternalDataChanged = pyqtSignal(list)
    sigIncreaseZ = pyqtSignal(int)
    sigDecreaseZ = pyqtSignal(int)

    properties = [
        "name",
        "hide",
        "lock",
        "x",
        "y",
        "alpha",
        "hflip",
        "vflip",
        "z",
    ]

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
        self._item = FrameSpriteItem(self._pixmap)
        self._name: str = ""
        self._x: float = 0
        self._y: float = 0
        self._vflip: bool = False
        self._hflip: bool = False
        self._alpha: int = 0
        self._z: int = 0
        self._hide: bool = False
        self._lock: bool = False
        self._alphaStep: bool = False

        self.name = name
        self.x = x
        self.y = y
        self.vflip = vflip
        self.hflip = hflip
        self.alpha = alpha

    def connected(self) -> None:
        self._item.subscribe(ItemEvent.zChanged, self.onItemZchanged)
        self._item.subscribe(ItemEvent.offsetChanged, self.onOffsetChanged)
        self._item.subscribe(ItemEvent.posChanged, self.onPosChanged)
        self._item.subscribe(ItemEvent.hFlipChanged, self.onHflipChanged)
        self._item.subscribe(ItemEvent.vFlipChanged, self.onVflipChanged)
        self._item.subscribe(ItemEvent.alphaChanged, self.onAlphaChanged)

        self.sigAddToScene.emit(self._item)
        self._item.addedToScene()

    def get(self, index: int) -> typing.Any:
        return getattr(self, self.properties[index])

    def set(self, index: int, value: typing.Any) -> None:
        setattr(self, self.properties[index], value)

    def changed(self, *indexes: Index) -> typing.List[typing.Tuple[int, Index]]:
        return [(self._z, index) for index in indexes]

    def copy(self):
        sprite = FrameSprite(
            self._name,
            self._pixmap,
            self._x,
            self._y,
            self._vflip,
            self._hflip,
            self._alpha,
        )
        sprite.hide = False
        sprite.lock = False
        sprite.name += "_copy"

        return sprite

    def delete(self) -> None:
        self._item.aboutToBeRemoved()
        self.sigDelFromScene.emit(self._item)

    def select(self) -> None:
        self._item.scene().clearSelection()
        self._item.setSelected(True)
        self._item.update()

    @staticmethod
    def count() -> int:
        return len(FrameSprite.properties)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def hide(self) -> bool:
        return self._hide

    @hide.setter
    def hide(self, value: bool) -> None:
        if self._hide != value:
            self._hide = value
            self._item.setVisible(not value)

    @property
    def lock(self) -> bool:
        return self._lock

    @lock.setter
    def lock(self, value: bool) -> None:
        if self._lock != value:
            self._lock = value
            self._item.setFlag(QGraphicsItem.ItemIsMovable, not value)
            self._item.setFlag(QGraphicsItem.ItemIsSelectable, not value)

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        if self._x != value:
            self._x = value
            self._item.setX(value)

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        if self._y != value:
            self._y = value
            self._item.setY(value)

    @property
    def alpha(self) -> int:
        return self._alpha

    @alpha.setter
    def alpha(self, value: int) -> None:
        if self._alpha != value:
            self._alpha = value
            self._item.setPixmap(Image.setAlpha(value, self._pixmap))

    @property
    def hflip(self) -> bool:
        return self._hflip

    @hflip.setter
    def hflip(self, value: bool) -> None:
        if self._hflip != value:
            Image.flipHorizontal(self._item)
            self._item.flipChanged()
        self._hflip = value

    @property
    def vflip(self) -> bool:
        return self._vflip

    @vflip.setter
    def vflip(self, value: bool) -> None:
        if self._vflip != value:
            Image.flipVertical(self._item)
            self._item.flipChanged()
        self._vflip = value

    @property
    def z(self) -> int:
        return self._z

    @z.setter
    def z(self, value: int) -> None:
        if self._z != value:
            self._z = value
            self._item.setZValue(value)

    def onItemZchanged(self, z: int) -> None:
        if z > self._z:
            self.sigIncreaseZ.emit(self._z)
        else:
            self.sigDecreaseZ.emit(self._z)

    def onPosChanged(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

        self.sigInternalDataChanged.emit(self.changed(Index.X, Index.Y))

    def onOffsetChanged(self, x: float, y: float) -> None:
        self.x += x
        self.y += y

        self.sigInternalDataChanged.emit(self.changed(Index.X, Index.Y))

    def onHflipChanged(self) -> None:
        self.hflip = not self._hflip
        self.sigInternalDataChanged.emit(self.changed(Index.Hflip))

    def onVflipChanged(self) -> None:
        self.vflip = not self._vflip
        self.sigInternalDataChanged.emit(self.changed(Index.Vflip))

    def onAlphaChanged(self) -> None:
        if self._alphaStep:
            self.alpha = 0
            self._alphaStep = False
        else:
            self._alphaStep = True
            self.alpha = 90

        self.sigInternalDataChanged.emit(self.changed(Index.Alpha))
