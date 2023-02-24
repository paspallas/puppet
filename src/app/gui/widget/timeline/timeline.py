from enum import IntEnum
import typing

import grid
from PyQt5.QtCore import Qt, QRectF, QPointF, QPoint, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (
    QGraphicsView,
    QGraphicsScene,
    QGraphicsItem,
    QGraphicsRectItem,
    QGraphicsObject,
    QGraphicsDropShadowEffect,
    QStyleOptionGraphicsItem,
    QWidget,
    QGraphicsSceneMouseEvent,
    QGraphicsSceneHoverEvent,
    qApp,
)
from PyQt5.QtGui import (
    QColor,
    QBrush,
    QPainter,
    QPen,
    QWheelEvent,
    QFontMetrics,
    QKeyEvent,
)

from grid import Grid
from key_frame_item import KeyFrameItem
from play_head_item import PlayHeadItem
from time_ruler import TimeRuler


class TimeLineScene(QGraphicsScene):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(0, 0, 1200, 400)


class TimeLineView(QGraphicsView):
    def __init__(
        self, scene: QGraphicsScene, parent: typing.Optional[QWidget] = None
    ) -> None:
        super().__init__(scene, parent)

        self.setAlignment(Qt.AlignTop)
        self.setStyleSheet("background-color: rgb(43, 42, 51);")
        self.setMouseTracking(True)
        self.setRenderHint(QPainter.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.centerOn(0, 0)

        self._playHead = PlayHeadItem()
        self.scene().addItem(self._playHead)
        self.scene().sceneRectChanged.connect(
            lambda rect: self._playHead.onSceneRectHeightChange(rect.height())
        )

        self._timeRuler = TimeRuler()
        Grid.computeGrid(self.scene().sceneRect(), [])
        self.scalings = 0

        self._makeConnections()

    def _makeConnections(self) -> None:
        self._playHead.sigPlayHeadPositionChange.connect(
            self._timeRuler.onPlayBackPositionChange
        )
        self._playHead.sigPlayHeadPositionChange.connect(self.onPlayHeadPositionChange)

    def drawBackground(self, painter: QPainter, rect: QRectF) -> None:
        Grid.paint(painter)
        self._timeRuler.paint(painter, rect, self.scene().width(), self.font())

    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.key() in [Qt.Key_Left, Qt.Key_A]:
            self._playHead.rewind()
        elif e.key() in [Qt.Key_Right, Qt.Key_D]:
            self._playHead.advance()
        else:
            super().keyPressEvent(e)

    def wheelEvent(self, e: QWheelEvent) -> None:
        if e.modifiers() & Qt.Modifier.CTRL:
            degs = e.angleDelta().y() / 8
            steps = degs / 15
            self.scalings += steps

            if self.scalings * steps < 0:
                self.scalings = steps

            factor = 1.0 + (self.scalings / 160.0)
            self.scale(factor, 1.0)
        else:
            super().wheelEvent(e)

    @pyqtSlot(float)
    def onPlayHeadPositionChange(self, pos: float) -> None:
        if pos >= self.viewport().rect().center().x() - grid.__xoffset__:
            self.centerOn(
                self._playHead.x(),
                self.mapToScene(self.viewport().rect()).boundingRect().center().y(),
            )
