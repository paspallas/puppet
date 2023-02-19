import typing

import grid
from PyQt5.QtCore import QLineF, QPointF, QRectF, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPainter, QPainterPath, QPen
from PyQt5.QtWidgets import (
    QGraphicsItem,
    QGraphicsObject,
    QGraphicsSceneMouseEvent,
    QStyleOptionGraphicsItem,
    QWidget,
)


class PlayHeadItem(QGraphicsObject):
    __color__ = QColor(50, 205, 50)
    __shadow__ = QColor(60, 205, 60, 200)
    __size__ = grid.__width__ / 2

    def __init__(self, x: float) -> None:
        super().__init__()

        self._rect = QRectF(0, 0, self.__size__, self.__size__)
        self._lineX = self._rect.width() / 2 - 1.5

        self.setX(x)
        self.setY(0)

        flags = (
            QGraphicsItem.ItemIsSelectable
            | QGraphicsItem.ItemSendsScenePositionChanges
            | QGraphicsItem.ItemIsMovable
            | QGraphicsItem.ItemIgnoresTransformations
        )
        self.setFlags(flags)
        self.setZValue(10000)

    def boundingRect(self) -> QRectF:
        return self._rect

    def itemChange(
        self, change: QGraphicsItem.GraphicsItemChange, value: typing.Any
    ) -> typing.Any:
        if change == QGraphicsItem.ItemPositionChange and self.scene():
            return QPointF(
                grid.alignToGrid(value.x()) + grid.__width__ / 4, self.pos().y()
            )

        return super().itemChange(change, value)

    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget
    ) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(self.__shadow__, 0, Qt.SolidLine)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.setBrush(self.__color__)

        rect = QRectF(self._lineX, 0, 1, widget.height())
        painter.drawRect(rect)

        # painter.drawLine(
        #     QPointF(self._lineX, 0),
        #     QPointF(self._lineX, widget.height()),
        # )
        # pen.setColor(self.__shadow__)
        # painter.setPen(pen)
        # painter.drawLine(
        #     QPointF(self._lineX + 0.5, 0), QPointF(self._lineX + 0.5, widget.height())
        # )

        painter.setBrush(self.__color__)
        painter.drawRoundedRect(
            self._rect,
            self.__size__ / 2,
            self.__size__ / 2,
        )
