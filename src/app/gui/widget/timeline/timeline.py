from enum import IntEnum
import typing

import grid
from PyQt5.QtCore import Qt, QRectF, QPointF, QPoint, pyqtSignal
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
from PyQt5.QtGui import QColor, QBrush, QPainter, QPen, QWheelEvent, QFontMetrics

from grid import Grid
from key_frame_item import KeyFrameItem
from play_head_item import PlayHeadItem
from time_ruler import TimeRuler


class TimeLineScene(QGraphicsScene):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(0, 0, 2000, 200)


class TimeLineView(QGraphicsView):
    def __init__(self, scene: QGraphicsScene, parent) -> None:
        super().__init__(scene, parent)

        self.setAlignment(Qt.AlignTop)
        self.setMouseTracking(True)
        self.setRenderHint(QPainter.Antialiasing)
        self.setOptimizationFlag(QGraphicsView.DontAdjustForAntialiasing)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.centerOn(0, 0)

        self._playHead = PlayHeadItem()
        self.scene().addItem(self._playHead)

        self._timeRuler = TimeRuler()
        Grid.computeGrid(self.scene().sceneRect())
        self.scalings = 0

        self._makeConnections()

    def _makeConnections(self) -> None:
        self._playHead.sigPlayHeadPositionChange.connect(
            self._timeRuler.onPlayBackPositionChange
        )

    def drawBackground(self, painter: QPainter, rect: QRectF) -> None:
        Grid.paint(painter)
        self._timeRuler.paint(painter, rect, self.scene().width(), self.font())

    def wheelEvent(self, e: QWheelEvent) -> None:
        if e.modifiers() & Qt.Modifier.CTRL:
            degs = e.angleDelta().y() / 8
            steps = degs / 15
            self.scalings += steps

            if self.scalings * steps < 0:
                self.scalings = steps

            factor = 1.0 + (self.scalings / 160.0)
            self.scale(factor, 1.0)
