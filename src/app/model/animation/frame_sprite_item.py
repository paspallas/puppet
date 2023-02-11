import typing
from enum import IntEnum

from PyQt5.QtCore import QPoint, Qt, QTimer, QVariant, pyqtSlot
from PyQt5.QtGui import QColor, QKeyEvent, QPainter, QPen, QPixmap
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

        self._dashOffset = 0
        self._timer = QTimer()
        self._timer.setInterval(166)
        self._timer.timeout.connect(self.animateDashOffset)
        self._timer.start()

    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.key() == Qt.Key.Key_Q:
            z = int(self.zValue()) + 1
            self.publish(ItemEvent.zChanged, z)

        elif e.key() == Qt.Key_E:
            z = int(self.zValue() - 1)
            self.publish(ItemEvent.zChanged, z)

        elif e.key() == Qt.Key_V:
            self.publish(ItemEvent.vFlipChanged)
        elif e.key() == Qt.Key_H:
            self.publish(ItemEvent.hFlipChanged)
        elif e.key() in [Qt.Key_Left, Qt.Key_A]:
            self.publish(ItemEvent.offsetChanged, -1, 0)
        elif e.key() in [Qt.Key_Right, Qt.Key_D]:
            self.publish(ItemEvent.offsetChanged, 1, 0)
        elif e.key() in [Qt.Key_Up, Qt.Key_W]:
            self.publish(ItemEvent.offsetChanged, 0, -1)
        elif e.key() in [Qt.Key_Down, Qt.Key_S]:
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

    def mousePressEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        self.setCursor(Qt.SizeAllCursor)
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        self.setCursor(Qt.ArrowCursor)
        super().mouseReleaseEvent(e)

    def animateDashOffset(self) -> None:
        self._dashOffset -= 1
        self.update()

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
            pen = QPen(Qt.magenta, 0, Qt.DashLine, Qt.SquareCap)
            pen.setDashOffset(self._dashOffset)
            painter.setPen(pen)
            painter.drawPath(self.shape().simplified())
