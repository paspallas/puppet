import typing

import grid
from PyQt5.QtCore import QLineF, QPointF, QRectF, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QColor, QPainter, QPainterPath, QPen, QKeyEvent
from PyQt5.QtWidgets import (
    QGraphicsItem,
    QGraphicsObject,
    QGraphicsSceneMouseEvent,
    QStyleOptionGraphicsItem,
    QWidget,
)


class PlayHeadItem(QGraphicsObject):
    __color__ = QColor(50, 205, 50)
    __shadow__ = QColor(20, 20, 20, 200)
    __size__ = grid.__width__

    sigPlayHeadPositionChange = pyqtSignal(float)

    def __init__(self, x: float) -> None:
        super().__init__()

        self._rect = QRectF(-self.__size__ / 2, 0, self.__size__, self.__size__)
        self.setX(x)
        self.setY(23)

        flags = (
            QGraphicsItem.ItemIsSelectable
            | QGraphicsItem.ItemIsFocusable
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
            x = grid.Grid.alignTo(value.x())
            # x = grid.Grid.alignTo(value.x()) + grid.__width__ / 4
            self.sigPlayHeadPositionChange.emit(x)

            return QPointF(x, self.pos().y())

        return super().itemChange(change, value)

    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.key() in [Qt.Key_A, Qt.Key_Left]:
            self.setX(self.x() - grid.__width__)
        elif e.key() in [Qt.Key_D, Qt.Key_Right]:
            self.setX(self.x() + grid.__width__)
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
            self.scene().sceneRect().height(),
        )
        painter.drawLine(line)
        pen.setColor(self.__shadow__)
        painter.setPen(pen)
        painter.drawRoundedRect(self._rect, 1, 1, Qt.AbsoluteSize)

    @pyqtSlot(int)
    def setPlaybackPosition(frame: int) -> None:
        NotImplemented
