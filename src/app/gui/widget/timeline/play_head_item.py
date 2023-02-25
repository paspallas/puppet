import typing

import grid
import time_scale
from PyQt5.QtCore import QLineF, QPointF, QRectF, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QColor, QKeyEvent, QPainter, QPen
from PyQt5.QtWidgets import (
    QGraphicsDropShadowEffect,
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
        self.setY(time_scale.__height__)

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

        fx = QGraphicsDropShadowEffect()
        fx.setXOffset(1)
        fx.setYOffset(1)
        self._marker.setGraphicsEffect(fx)

        self._currentY = time_scale.__height__
        self._dragOrigin = 0

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

    def mousePressEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        if e.button() == Qt.LeftButton:
            self._dragOrigin = e.scenePos().x()
        super().mousePressEvent(e)

    def mouseMoveEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        if (e.buttons() & Qt.LeftButton) == Qt.LeftButton:
            delta = e.scenePos().x() - self._dragOrigin

            if abs(delta) >= grid.__pxPerFrame__:
                if delta > 0:
                    self.advance()
                else:
                    self.rewind()
                self._dragOrigin = e.scenePos().x()
        else:
            super().mouseMoveEvent(e)

    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget
    ) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(__shadow__, 0, Qt.SolidLine)
        pen.setCosmetic(True)
        painter.setPen(pen)
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
        self._currentY = time_scale.__height__ + scroll
        self.setY(self._currentY)
