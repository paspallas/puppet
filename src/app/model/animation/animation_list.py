import typing

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from .animation import Animation


class AnimationList(QObject):
    def __init__(self):
        super().__init__()

        self._animations: typing.List[Animation] = []

    def set(self, index: int, value: str) -> None:
        self._animations[index].name = value

    def get(self, index: int) -> str:
        return self._animations[index].name

    def add(self) -> None:
        self._animations.append(Animation("new animation"))

    def delete(self, index: int) -> None:
        if index < len(self._animations):
            self._animations.pop(index)

    def source(self, id: str) -> typing.List:
        for animation in self._animations:
            if animation.name == id:
                return animation

    def __len__(self) -> int:
        return len(self._animations)
