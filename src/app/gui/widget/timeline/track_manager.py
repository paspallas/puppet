import typing
import random

import grid
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QColor

from track_item import TrackItem


def randomColor() -> QColor:
    color = lambda: [
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    ]
    return QColor(*color())


class TrackManager(QObject):
    def __init__(self, scene: QGraphicsScene) -> None:
        super().__init__()

        self._scene = scene
        self._tracks: typing.List[TrackItem] = list()

    def newTrack(self) -> TrackItem:
        count = len(self._tracks)
        y = grid.__yoffset__ + count * grid.__trackHeight__ * 3

        t = TrackItem(count, y=y, color=randomColor())
        t.sigCollapseChange.connect(self.onTrackCollapseChange)

        self._tracks.append(t)
        self._scene.addItem(t)

        return t

    @pyqtSlot(bool, int)
    def onTrackCollapseChange(self, collapsed: bool, index: int) -> None:
        t = self._tracks[index]
        offset = len(t.childItems()) * grid.__trackHeight__

        if collapsed:
            offset = -offset

        self._setChildVisible(not collapsed, index)
        self._updateTrackPositions(offset, index)

    def _updateTrackPositions(self, offset: int, index: int) -> None:
        for t in self._tracks[index + 1 :]:
            t.setY(t.y() + offset)

    def _setChildVisible(self, visible: bool, index: int) -> None:
        t = self._tracks[index]
        for child in t.childItems():
            child.setVisible(visible)
