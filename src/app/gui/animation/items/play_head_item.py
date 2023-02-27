import typing

from PyQt5.QtCore import QLineF, QPointF, QRectF, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QColor, QFontMetrics, QKeyEvent, QPainter, QPen
from PyQt5.QtWidgets import (
    QGraphicsItem,
    QGraphicsLineItem,
    QGraphicsObject,
    QGraphicsSceneMouseEvent,
    QStyleOptionGraphicsItem,
    QWidget,
)

from ..grid import Grid, __midFrame__, __pxPerFrame__, __xoffset__
from . import time_scale_item as scale

__color__ = QColor("#2A82DA")
__border__ = QColor("#5680C2")
__width__ = 30
__height__ = 20


class PlayHeadItem(QGraphicsObject):
    sigPlayHeadPositionChange = pyqtSignal(float)

    def __init__(self, fm: QFontMetrics) -> None:
        super().__init__()

        flags = (
            QGraphicsItem.ItemIsFocusable | QGraphicsItem.ItemSendsScenePositionChanges
        )
        self.setFlags(flags)
        self.setZValue(10000)

        self._rect = QRectF(-__width__ / 2, 0, __width__, __height__)

        self.setX(Grid.alignTo(__xoffset__))
        self.setY(scale.__textY__)
        self._currentY = scale.__textY__

        # Draw a line in the middle of the current frame
        self._marker = QGraphicsLineItem(0, 0, 0, 0, self)
        self._marker.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self._marker.setFlag(QGraphicsItem.ItemStacksBehindParent)
        self._marker.setX(__midFrame__)
        self._marker.setY(__height__)
        self._marker.setPen(__color__)

        self._fm = fm
        self._label = ""
        self._labelRect = self._rect

    def boundingRect(self) -> QRectF:
        return self._rect

    def itemChange(
        self, change: QGraphicsItem.GraphicsItemChange, value: typing.Any
    ) -> typing.Any:
        if change == QGraphicsItem.ItemPositionChange and self.scene():
            # vertical scrolling triggers y position changes
            if self.x() == value.x():
                return QPointF(value.x(), self._currentY)

            x = self._correctPosition(value.x())
            self.updateLabel(x)

            self.sigPlayHeadPositionChange.emit(x)
            return QPointF(x, self._currentY)

        return super().itemChange(change, value)

    def _correctPosition(self, x: float) -> float:
        max_ = self.scene().sceneRect().right()

        if x > max_ - __pxPerFrame__:
            x = max_ - __pxPerFrame__

        return Grid.alignTo(x)

    def updateLabel(self, x: float) -> None:
        self._label = f"{Grid.pixelToFrame(x)}"

        # align the text center with a tick mark
        self._labelRect = QRectF(
            self._fm.boundingRect(self._label).translated(__midFrame__, 0)
        )
        self._labelRect.translate(
            -self._labelRect.width() / 2, self._labelRect.height()
        )

    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget
    ) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(__border__)
        painter.setBrush(__color__)
        painter.drawRoundedRect(
            self._rect.adjusted(__midFrame__, 0, __midFrame__, 0), 3, 3, Qt.AbsoluteSize
        )

        painter.setPen(Qt.white)
        painter.drawText(self._labelRect, self._label)

    @pyqtSlot()
    def advance(self) -> None:
        self.setX(self.x() + __pxPerFrame__)

    @pyqtSlot()
    def rewind(self) -> None:
        self.setX(self.x() - __pxPerFrame__)

    @pyqtSlot(float)
    def setPlaybackPosition(self, x: float) -> None:
        self.setX(x)

    @pyqtSlot(float)
    def onSceneRectHeightChange(self, height: float) -> None:
        self._marker.setLine(0, 0, 0, height - scale.__height__)

    @pyqtSlot(int)
    def onVerticalScrollBarChange(self, scroll: int) -> None:
        # Keep the item in a fixed y position
        self._currentY = scroll + scale.__textY__
        self.setY(self._currentY)
