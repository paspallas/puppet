from dataclasses import astuple, dataclass
from typing import NamedTuple


@dataclass(frozen=True, slots=True)
class Frame:
    class TopLeft(NamedTuple):
        x: int
        y: int

    class Size(NamedTuple):
        w: int
        h: int

    class Rect(NamedTuple):
        x: int
        y: int
        w: int
        h: int

    name: str
    x: int
    y: int
    w: int
    h: int

    def topLeft(self) -> TopLeft:
        return self.TopLeft(self.x, self.y)

    def size(self) -> Size:
        return self.Size(self.w, self.h)

    def rect(self) -> Rect:
        return self.Rect(self.x, self.y, self.w, self.h)

    def __iter__(self):
        return iter(astuple(self))

    def __str__(self) -> str:
        return ", ".join([self.name, str(self.rect())])
