from dataclasses import astuple, dataclass
from pathlib import Path
from typing import Final, NamedTuple

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from spriteutil.spritesheet import SpriteSheet as Sheet


@dataclass(frozen=True, slots=True)
class Frame:

    TopLeft = NamedTuple("TopLeft", x=int, y=int)
    Size = NamedTuple("Size", w=int, h=int)
    Rect = NamedTuple("Rect", x=int, y=int, w=int, h=int)

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


class SpriteSheet:
    def __init__(self, path: str):

        self.path = path
        self.name = Path(self.path).stem
        self._frames: dict[str, Frame:Final] = dict()

        self._findFrames()

    def _findFrames(self):
        """Find all frames in the spritesheet"""

        sheet = Sheet(self.path)
        frames, _ = sheet.find_sprites()

        for i, frame in enumerate(frames):
            name = f"{self.name}_{i}"
            self._frames[name] = Frame(name, *frame.top_left, frame.width, frame.height)

    def __iter__(self):
        self._currentIndex = 0
        self._framesList = list(self._frames.values())
        return self

    def __next__(self):
        if self._currentIndex < len(self._framesList):
            frame = self._framesList[self._currentIndex]
            self._currentIndex += 1
            return frame
        raise StopIteration

    def __repr__(self) -> str:
        frames = "\n".join([str(frame) for frame in self.frames.values()])

        return f"SpriteSheet: path={self._path} frames=\n{frames}"


class SpriteSheetCollection(QObject):

    sigSpriteSheetAdded = pyqtSignal(SpriteSheet)

    def __init__(self):
        super().__init__()

        self._sheets: dict[str, SpriteSheet] = dict()

    @pyqtSlot(str)
    def addSpriteSheet(self, path: str):
        name = Path(path).stem

        if name in self._sheets:
            return

        sheet = SpriteSheet(path)
        self._sheets[name] = sheet

        self.sigSpriteSheetAdded.emit(sheet)

        # TODO this class should be two separate classess: a pure python class contained in a
        # qt model class

    @pyqtSlot(str)
    def delSpriteSheet(self, name: str):
        self._sheets.pop(name)
