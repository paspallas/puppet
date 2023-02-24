import typing
import random

import grid
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem
from PyQt5.QtGui import QColor

from track_item import TrackItem


def randomColor() -> QColor:
    color = [
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    ]
    return QColor(*color)


class TrackManager(QObject):
    def __init__(self, scene: QGraphicsScene) -> None:
        super().__init__()

        self._scene = scene
        self._tracks: typing.List[TrackItem] = list()

    def newTrack(self) -> TrackItem:
        track = TrackItem(
            len(self._tracks), y=self._computeTrackPosition(), color=randomColor()
        )
        track.sigCollapseChange.connect(self.onTrackCollapseChange)

        self._tracks.append(track)
        self._scene.addItem(track)
        self._updateSceneRect()

        return track

    def addPropertyTrack(self, parentTrack: int) -> None:
        track = QGraphicsRectItem(0, 0, 50, grid.__trackHeight__)
        track.setBrush(randomColor())

        self._tracks[parentTrack].addPropertyTrack(track)
        self._updateSceneRect()

    @pyqtSlot(bool, int)
    def onTrackCollapseChange(self, collapse: bool, index: int) -> None:
        track = self._tracks[index]

        # take the parent track height into account
        offset = track.expandedHeight() - grid.__trackHeight__

        if collapse:
            offset = -offset

        self._setChildVisible(not collapse, index)
        self._updateTrackPositions(offset, index)
        self._updateSceneRect()

    def _computeTrackPosition(self) -> float:
        pos = grid.__yoffset__

        for track in self._tracks:
            pos += track.trackHeight() + grid.__trackVSpacing__

        return pos

    def _itemsPerTrack(self) -> typing.List[int]:
        items = []

        for track in self._tracks:
            if track.isCollapsed():
                items.append(1)
            else:
                items.append(len(track.childItems()) + 1)

        return items

    def _updateTrackPositions(self, offset: int, index: int) -> None:
        # adjust all track positions below the collapsed/expanded one
        for t in self._tracks[index + 1 :]:
            t.setY(t.y() + offset)

    def _setChildVisible(self, visible: bool, index: int) -> None:
        track = self._tracks[index]
        for child in track.childItems():
            child.setVisible(visible)

    def _updateSceneRect(self) -> None:
        height = grid.__yoffset__

        for track in self._tracks:
            height += track.trackHeight() + grid.__trackVSpacing__

        r = self._scene.sceneRect()
        r.setHeight(height)
        self._scene.setSceneRect(r)
        grid.Grid.computeGrid(r, self._itemsPerTrack())
