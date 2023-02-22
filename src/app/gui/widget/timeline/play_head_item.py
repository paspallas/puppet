import typing

import grid
import time_ruler
from PyQt5.QtCore import QLineF, QPointF, QRectF, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QColor, QKeyEvent, QPainter, QPainterPath, QPen
from PyQt5.QtWidgets import (
    QGraphicsItem,
    QGraphicsObject,
    QGraphicsSceneMouseEvent,
    QStyleOptionGraphicsItem,
    QWidget,
)


class PlayHeadItem(QGraphicsObject):
    __color__ = QColor(120, 228, 87)
    __shadow__ = QColor(200, 200, 200, 255)
    __size__ = grid.__pxPerFrame__

    sigPlayHeadPositionChange = pyqtSignal(float)

    def __init__(self) -> None:
        super().__init__()

        self._rect = QRectF(-self.__size__ / 2, 0, self.__size__, self.__size__)
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

    def boundingRect(self) -> QRectF:
        return self._rect

    def itemChange(
        self, change: QGraphicsItem.GraphicsItemChange, value: typing.Any
    ) -> typing.Any:
        if change == QGraphicsItem.ItemPositionChange and self.scene():
            x = grid.Grid.alignTo(value.x(), self.__size__ / 2)
            self.sigPlayHeadPositionChange.emit(x)
            return QPointF(x, self.pos().y())

        return super().itemChange(change, value)

    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.key() in [Qt.Key_A, Qt.Key_Left]:
            self.setX(self.x() - (grid.__pxPerFrame__ + self.__size__ / 2))
        elif e.key() in [Qt.Key_D, Qt.Key_Right]:
            self.setX(self.x() + self.__size__ / 2)
        else:
            super().keyPressEvent(e)

    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget
    ) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(self.__color__, 0, Qt.SolidLine)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.setBrush(self.__color__)

        line = QLineF(
            self._rect.center().x(),
            self._rect.height() / 2,
            self._rect.center().x(),
            self.scene().sceneRect().height() - time_ruler.__height__,
        )
        painter.drawLine(line)
        pen.setColor(self.__shadow__)
        painter.setPen(pen)
        painter.drawRoundedRect(self._rect, 1, 1, Qt.AbsoluteSize)

    @pyqtSlot(int)
    def setPlaybackPosition(frame: int) -> None:
        NotImplemented
