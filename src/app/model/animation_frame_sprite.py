class FrameSprite:
    def __init__(self, name: str, x: int, y: int, vflip: bool, hflip: bool, alpha: int):
        self._name: str = name
        self._x: int = x
        self._y: int = y
        self._vflip: bool = vflip
        self._hflip: bool = hflip
        self._transparency: int = alpha
        self._zIndex: int = 0
        self._hide: bool = False
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

    @property
    def lock(self) -> bool:
        return self._lock

    @lock.setter
    def lock(self, value: bool):
        self._lock = value

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int):
        self._x = value

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

    def copy(self):
        item = FrameSprite(
            self.name,
            self.x,
            self.y,
            self.vflip,
            self.hflip,
            self.alpha,
        )
        item.zIndex = self.zIndex
        item.hide = self.hide
        item.lock = self.lock
        item.name += "_copy"
        return item
