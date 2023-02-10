import typing
from enum import IntEnum

from PyQt5.QtCore import Qt, QPoint, QTimer, QVariant
from PyQt5.QtGui import QBrush, QColor, QKeyEvent, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import (
    QGraphicsItem,
    QGraphicsPixmapItem,
    QGraphicsSceneMouseEvent,
    QGraphicsSceneWheelEvent,
    QWidget,
)

from ...util.pubsub import Publisher


class ItemEvent(IntEnum):
    posChanged = 0
    offsetChanged = 1
    zChanged = 2
    vFlipChanged = 3
    hFlipChanged = 4


class FrameSpriteItem(QGraphicsPixmapItem, Publisher):
    """A graphicsitem used for visualization and user interaction in the editor scene.

    QGraphicsItems can't inherit from QObject so an alternative publisher, subscriber
    interface is implemented. Using QGraphicsObject is discouraged in this particular
    scenario for performance considerations.
    """

    def __init__(self, pixmap: QPixmap) -> None:
        super().__init__(pixmap, None)

        self.setFlags(
            QGraphicsItem.ItemIsMovable
            | QGraphicsItem.ItemIsSelectable
            | QGraphicsItem.ItemIsFocusable
            | QGraphicsItem.ItemSendsGeometryChanges
            | QGraphicsItem.ItemSendsScenePositionChanges
        )

    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.key() == Qt.Key.Key_Q:
            z = int(self.zValue()) + 1
            self.publish(ItemEvent.zChanged, z)

        elif e.key() == Qt.Key_W:
            z = int(self.zValue() - 1)
            self.publish(ItemEvent.zChanged, z)

        elif e.key() == Qt.Key_V:
            self.publish(ItemEvent.vFlipChanged)
        elif e.key() == Qt.Key_H:
            self.publish(ItemEvent.hFlipChanged)
        elif e.key() == Qt.Key_Left:
            self.publish(ItemEvent.offsetChanged, -1, 0)
        elif e.key() == Qt.Key_Right:
            self.publish(ItemEvent.offsetChanged, 1, 0)
        elif e.key() == Qt.Key_Up:
            self.publish(ItemEvent.offsetChanged, 0, -1)
        elif e.key() == Qt.Key_Down:
            self.publish(ItemEvent.offsetChanged, 0, 1)
        else:
            super().keyPressEvent(e)

    def wheelEvent(self, e: QGraphicsSceneWheelEvent) -> None:
        if e.modifiers() & Qt.Modifier.ALT:
            if e.delta() > 0:
                z = int(self.zValue() - 1)
                self.publish(ItemEvent.zChanged, z)
            elif e.delta() < 0:
                z = int(self.zValue() + 1)
                self.publish(ItemEvent.zChanged, z)

    def itemChange(
        self, change: QGraphicsItem.GraphicsItemChange, value: typing.Any
    ) -> typing.Any:
        if change == QGraphicsItem.ItemPositionChange and self.scene():
            self.publish(ItemEvent.posChanged, value.x(), value.y())

        return super().itemChange(change, value)

    def paint(
        self,
        painter: QPainter,
        option,
        widget: QWidget = None,
    ) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, False)
        painter.drawPixmap(QPoint(), self.pixmap())

        if self.isSelected():
            pen = QPen(QColor(Qt.white), 0, Qt.DashLine, Qt.RoundCap, Qt.RoundJoin)
            pen.setCosmetic(True)
            painter.setPen(pen)
            painter.drawRect(self.boundingRect().adjusted(0.5, 0.5, 0, 0))
