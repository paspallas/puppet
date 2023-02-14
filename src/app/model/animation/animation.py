import typing

from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot

from ..animation_frame import AnimationFrame


class Animation(QObject):
    def __init__(self, name: str):
        super().__init__()

        self.name: str = name
        self._frames: typing.List[AnimationFrame] = []

    def add(self) -> None:
        self._frames.append(AnimationFrame())

    def delete(self, index: int) -> None:
        if index < len(self):
            self._frames.pop(index)

    def get(self, index: int) -> str:
        # TODO
        return f"{self.name}_{index}"

    def __len__(self) -> int:
        return len(self._frames)
