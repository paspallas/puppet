from typing import Any

from PyQt5.QtCore import QPointF, QRectF, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen
from PyQt5.QtWidgets import (
    QGraphicsItem,
    QGraphicsRectItem,
    QGraphicsSceneMouseEvent,
    QWidget,
)


class Rectangle(QGraphicsRectItem):

    """A rectangle used to delimit areas of interest in the scene"""

    def __init__(
        self,
        position: QPointF,
        rect: QRectF = None,
        parent: QGraphicsItem = None,
    ) -> None:
        super().__init__(rect, parent=parent)

        self._model = None

        self.setPos(position)
        flags = (
            QGraphicsItem.ItemIsSelectable
            | QGraphicsItem.ItemIsFocusable
            | QGraphicsItem.ItemSendsGeometryChanges
            | QGraphicsItem.ItemSendsScenePositionChanges
        )
        self.setFlags(flags)
        self.setAcceptHoverEvents(True)

    def _updateModel(self) -> None:
        rect = self.mapRectToScene(self.rect())
        # self._model.setPosition(QPointF(rect.x(), rect.y()))

    def setModel(self, model) -> None:
        self._model = model

    def paint(
        self,
        painter: QPainter,
        option,
        widget: QWidget = None,
    ) -> None:
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen(Qt.magenta, 0, Qt.SolidLine)
        brush = QBrush(QColor(Qt.transparent))

        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawRect(self.rect())

        # draw inner shadow
        pen.setColor(QColor(100, 100, 100, 100))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawRect(self.rect().adjusted(0.5, 0.5, -0.5, -0.5))

    def mouseMoveEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        if e.buttons() & Qt.LeftButton:
            super().mouseMoveEvent(e)

    @pyqtSlot(QRectF)
    def resize(self, change: QRectF) -> None:
        self.prepareGeometryChange()
        self.setRect(change)

    @pyqtSlot(QPointF)
    def position(self, change: QPointF) -> None:
        self.prepareGeometryChange()
        self.setRect(
            self.rect().adjusted(change.x(), change.y(), change.x(), change.y())
        )

        self._updateModel()
