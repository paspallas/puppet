import typing

from PyQt5.QtCore import QObject, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsScene

from ...util import Image
from . import grid
from .items import TrackItem


class TrackManager(QObject):
    def __init__(self, scene: QGraphicsScene) -> None:
        super().__init__()

        self._scene = scene
        self._tracks: typing.List[TrackItem] = list()

    def newTrack(self) -> TrackItem:
        track = TrackItem(
            len(self._tracks), y=self._computeTrackPosition(), color=Image.randomColor()
        )
        track.sigCollapseChange.connect(self.onTrackCollapseChange)

        self._tracks.append(track)
        self._scene.addItem(track)
        self._updateSceneRect()

        return track

    def addPropertyTrack(self, parentTrack: int) -> None:
        track = QGraphicsRectItem(0, 0, 50, grid.__trackHeight__)
        track.setBrush(Image.randomColor())

        self._tracks[parentTrack].addPropertyTrack(track)
        self._updateSceneRect()

    @pyqtSlot(bool, int)
    def onTrackCollapseChange(self, collapse: bool, index: int) -> None:
        track = self._tracks[index]
        offset = -track.childBoxHeight if collapse else track.childBoxHeight

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

    def _updateSceneRect(self) -> None:
        height = grid.__yoffset__

        for track in self._tracks:
            height += track.trackHeight() + grid.__trackVSpacing__

        r = self._scene.sceneRect()
        r.setHeight(height)
        self._scene.setSceneRect(r)
        grid.Grid.computeGrid(r, self._itemsPerTrack())
