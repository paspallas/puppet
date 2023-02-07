import typing

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from .animation import Animation


class AnimationList(QObject):
    def __init__(self):
        super().__init__()

        self._animations: typing.List[Animation] = []

    def set(self, index: int, value: str) -> None:
        pass

    def get(self, index: int) -> typing.Any:
        pass

    def __len__(self) -> int:
        return len(self._animations)
