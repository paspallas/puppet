import typing

import grid
import time_ruler
from PyQt5.QtCore import QLineF, QPointF, QRectF, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QColor, QKeyEvent, QPainter, QPainterPath, QPen
from PyQt5.QtWidgets import (
    QGraphicsItem,
    QGraphicsLineItem,
    QGraphicsObject,
    QGraphicsSceneMouseEvent,
    QStyleOptionGraphicsItem,
    QWidget,
)

__color__ = QColor(220, 25, 29)
__shadow__ = QColor(65, 0, 0, 220)
__size__ = grid.__pxPerFrame__


class PlayHeadItem(QGraphicsObject):
    sigPlayHeadPositionChange = pyqtSignal(float)

    def __init__(self) -> None:
        super().__init__()

        self._rect = QRectF(-__size__ / 2, 0, __size__, __size__)
        self.setX(grid.__xoffset__)
        self.setY(time_ruler.__height__)

        flags = (
            QGraphicsItem.ItemIsSelectable
            | QGraphicsItem.ItemIsFocusable
            | QGraphicsItem.ItemSendsScenePositionChanges
            | QGraphicsItem.ItemIsMovable
        )
        self.setFlags(flags)
        self.setZValue(10000)

        self._marker = QGraphicsLineItem(0, __size__, 0, 0, self)
        self._marker.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self._marker.setPen(__color__)

    def boundingRect(self) -> QRectF:
        return self._rect

    def itemChange(
        self, change: QGraphicsItem.GraphicsItemChange, value: typing.Any
    ) -> typing.Any:
        if change == QGraphicsItem.ItemPositionChange and self.scene():
            x = grid.Grid.alignTo(value.x(), __size__ / 2)
            self.sigPlayHeadPositionChange.emit(x)
            return QPointF(x, self.pos().y())

        return super().itemChange(change, value)

    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget
    ) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(__shadow__, 0, Qt.SolidLine)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.setBrush(__color__)
        painter.drawRoundedRect(self._rect, 1, 1, Qt.AbsoluteSize)

    def advance(self) -> None:
        self.setX(self.x() + __size__ / 2)

    def rewind(self) -> None:
        self.setX(self.x() - (grid.__pxPerFrame__ + __size__ / 2))

    @pyqtSlot(int)
    def setPlaybackPosition(frame: int) -> None:
        pass

    @pyqtSlot(float)
    def onSceneRectHeightChange(self, height: float) -> None:
        self._marker.setLine(0, __size__, 0, height - time_ruler.__height__)
