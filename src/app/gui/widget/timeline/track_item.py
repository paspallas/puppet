import typing

import grid
from PyQt5.QtCore import (
    QPointF,
    QRectF,
    Qt,
    pyqtSignal,
    pyqtSlot,
)
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import (
    QGraphicsItem,
    QGraphicsObject,
    QGraphicsRectItem,
    QStyleOptionGraphicsItem,
    QWidget,
)


class TrackItem(QGraphicsObject):
    sigCollapseChange = pyqtSignal(bool, int)

    def __init__(
        self,
        index: int,
        x: float = 0.0,
        y: float = 0.0,
        span: float = 200,
        color: QColor = QColor(Qt.white),
    ) -> None:
        super().__init__()
        self._index = index
        self._y = 0.0
        self._color = color
        self._collapsed = False
        self._rect = QRectF(0, 0, span, grid.__trackHeight__)

        flags = (
            QGraphicsItem.ItemIsSelectable
            | QGraphicsItem.ItemIsMovable
            | QGraphicsItem.ItemSendsScenePositionChanges
        )
        self.setFlags(flags)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.setX(grid.__xoffset__ + x)
        self.setY(y)

        self.rect1 = QGraphicsRectItem(0, 20, 100, 20, self)
        self.rect1.setFlag(QGraphicsItem.ItemIsSelectable)
        self.rect1.setBrush(Qt.red)
        self.rect2 = QGraphicsRectItem(0, 40, 120, 20, self)
        self.rect2.setBrush(Qt.green)

    def trackHeight(self) -> float:
        height = 0
        for child in self.childItems():
            height += grid.__trackHeight__ if child.isVisible() else 0

        return height

    def itemChange(
        self, change: QGraphicsItem.GraphicsItemChange, value: typing.Any
    ) -> typing.Any:
        if change == QGraphicsItem.ItemPositionChange and self.scene():
            return QPointF(grid.Grid.alignTo(value.x()), self._y)

        return super().itemChange(change, value)

    def setY(self, y: float) -> None:
        self._y = y
        super().setY(y)

    def boundingRect(self) -> QRectF:
        if self._collapsed:
            return self._rect

        return self._rect.adjusted(0, 0, 0, self.trackHeight())

    def mousePressEvent(self, e) -> None:
        if e.buttons() == Qt.LeftButton:
            self._collapsed = not self._collapsed
            self.sigCollapseChange.emit(self._collapsed, self._index)
        super().mousePressEvent(e)

    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget
    ) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self._color)
        painter.setPen(Qt.NoPen)

        if not self._collapsed:
            painter.save()
            painter.setOpacity(0.5)
            painter.drawRect(self.boundingRect())
            painter.restore()

        painter.setPen(Qt.black)
        painter.drawRect(self._rect)
