import typing

from PyQt5.QtCore import QLineF, QPointF, QRectF, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QColor, QKeyEvent, QPainter, QPen
from PyQt5.QtWidgets import (
    QGraphicsItem,
    QGraphicsLineItem,
    QGraphicsObject,
    QGraphicsSceneMouseEvent,
    QStyleOptionGraphicsItem,
    QWidget,
)

from .. import grid
from . import time_scale_item

__color__ = QColor(240, 25, 29)
__shadow__ = QColor(65, 0, 0, 220)
__size__ = grid.__pxPerFrame__


class PlayHeadItem(QGraphicsObject):
    sigPlayHeadPositionChange = pyqtSignal(float)

    def __init__(self) -> None:
        super().__init__()

        self._rect = QRectF(-__size__ / 2, 0, __size__, __size__)
        self.setX(grid.Grid.alignTo(grid.__xoffset__, __size__ / 2))
        self.setY(time_scale_item.__height__)

        flags = (
            QGraphicsItem.ItemIsFocusable | QGraphicsItem.ItemSendsScenePositionChanges
        )
        self.setFlags(flags)
        self.setZValue(10000)

        self._marker = QGraphicsLineItem(0, __size__, 0, 0, self)
        self._marker.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self._marker.setPen(__color__)

        self._currentY = time_scale_item.__height__

        self._pen = QPen(__shadow__, 0, Qt.SolidLine)
        self._pen.setCosmetic(True)

    def boundingRect(self) -> QRectF:
        return self._rect

    def itemChange(
        self, change: QGraphicsItem.GraphicsItemChange, value: typing.Any
    ) -> typing.Any:
        if change == QGraphicsItem.ItemPositionChange and self.scene():
            # vertical scrolling triggers y position changes
            if self.x() == value.x():
                return QPointF(value.x(), self._currentY)

            max_ = self.scene().sceneRect().right()
            x = value.x() if value.x() < max_ - __size__ else max_ - __size__
            x = grid.Grid.alignTo(x, __size__ / 2)

            self.sigPlayHeadPositionChange.emit(x)
            return QPointF(x, self._currentY)

        return super().itemChange(change, value)

    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget
    ) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(self._pen)
        painter.setBrush(__color__)
        painter.drawRoundedRect(self._rect, 1, 1, Qt.AbsoluteSize)

    @pyqtSlot()
    def advance(self) -> None:
        self.setX(self.x() + __size__ / 2)

    @pyqtSlot()
    def rewind(self) -> None:
        self.setX(self.x() - (grid.__pxPerFrame__ + __size__ / 2))

    @pyqtSlot(float)
    def setPlaybackPosition(self, x: float) -> None:
        self.setX(x)

    @pyqtSlot(float)
    def onSceneRectHeightChange(self, height: float) -> None:
        self._marker.setLine(0, __size__, 0, height - self.y())

    @pyqtSlot(int)
    def onVerticalScrollBarChange(self, scroll: int) -> None:
        # Keep the item in a fixed y position
        self._currentY = time_scale_item.__height__ + scroll
        self.setY(self._currentY)
