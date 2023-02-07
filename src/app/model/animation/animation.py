import typing

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from .frame import AnimationFrame


class Animation(QObject):
    def __init__(self):
        super().__init__()

        self._name: str = None
        self._frames: typing.List[AnimationFrame] = []

    def __len__(self) -> int:
        return len(self._frames)
