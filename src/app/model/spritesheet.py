from pathlib import Path
from typing import Final

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QColor, QPixmap
from spriteutil.spritesheet import SpriteSheet as Sheet

from .frame import Frame
from .sprite import Sprite


class SpriteSheet:
    def __init__(self, path: str):

        self.path = path
        self.name = Path(self.path).stem

        self._pixmap = QPixmap(path)
        self._frames: dict[int, Frame:Final] = dict()

        sheet = Sheet(path)
        self._extractFrames(sheet)
        self._pixmap.setMask(
            self._pixmap.createMaskFromColor(QColor(*sheet.background_color))
        )

    def countFrames(self) -> int:
        """Get the number of frames in the spritesheet

        Returns:
            int: Number of frames
        """

        return len(self._frames.values())

    def spriteFromFrame(self, frame: Frame) -> Sprite:
        """Create a sprite from a frame

        Args:
            frame (Frame): Frame object

        Returns:
            Sprite: The sprite item
        """

        return Sprite(self._pixmap.copy(*frame.rect()), *frame.topLeft())

    def spriteFromFrameIndex(self, index: int) -> Sprite:
        """Create a sprite from a frame index

        Args:
            index (int): Frame index

        Returns:
            Sprite: The sprite item
        """

        frame = self._frames.get(index, None)

        if frame:
            return self.spriteFromFrame(frame)

    def sprites(self) -> list[Sprite]:
        """Get all frames in the spritesheet as independent sprites

        Returns:
            list[Sprite]: Collection of all the sprites
        """

        return [self.spriteFromFrame(frame) for frame in self._frames.values()]

    def _extractFrames(self, sheet: Sheet) -> None:
        """Extract all frames in the spritesheet"""

        frames, _ = sheet.find_sprites()

        for i, frame in enumerate(frames):
            name = f"{self.name}_{i}"
            self._frames[i] = Frame(name, *frame.top_left, frame.width, frame.height)

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


class SpriteSheetCollectionModel(QObject):

    sigSpriteSheetAdded = pyqtSignal(SpriteSheet)
    sigSpriteSheetRemoved = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self._sheets: dict[str, SpriteSheet] = dict()

    def addSpriteSheet(self, path: str):
        """Add a new spritesheet to the collection

        Args:
            path (str): spritesheet image path
        """
        name = Path(path).stem

        if name in self._sheets:
            return

        sheet = SpriteSheet(path)
        self._sheets[name] = sheet

        self.sigSpriteSheetAdded.emit(sheet)

    def delSpriteSheet(self, name: str):
        """Remove a spritesheet from the collection

        Args:
            name (str): spritesheet identifier
        """
        self._sheets.pop(name)
        self.sigSpriteSheetRemoved.emit(name)
