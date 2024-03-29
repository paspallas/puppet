import typing
from enum import IntEnum

from PyQt5.QtCore import QLineF, QPoint, QPointF, QRectF, Qt, QVariant, pyqtSlot
from PyQt5.QtGui import QColor, QKeyEvent, QPainter, QPainterPath, QPen, QPixmap
from PyQt5.QtWidgets import (
    QAction,
    QGraphicsItem,
    QGraphicsPixmapItem,
    QGraphicsSceneContextMenuEvent,
    QGraphicsSceneMouseEvent,
    QGraphicsSceneWheelEvent,
    QMenu,
    QWidget,
)

from ...util.image import Image
from ...util.pubsub import Publisher
from .item_context_menu import ItemMenuDelegate
from .overlay import Overlay


class ItemEvent(IntEnum):
    posChanged = 0
    zChanged = 1
    vFlipChanged = 2
    hFlipChanged = 3
    enableHint = 4
    disableHint = 5


class FrameSpriteItem(QGraphicsPixmapItem, Publisher):
    """A graphicsitem used for visualization and user interaction in the editor scene.

    QGraphicsItems can't inherit from QObject so an alternative publisher - subscriber
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

        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)

        # make the item selectable regardless of transparency level
        self._outline = Image.outline(pixmap)

        self._overlay = Overlay(
            self.boundingRect(),
            self._outline,
        )
        self._overlay.setZValue(self.zValue())

    def addedToScene(self):
        self.scene().addItem(self._overlay)

    def aboutToBeRemoved(self) -> None:
        self.scene().removeItem(self._overlay)

    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.isAutoRepeat():
            return super().keyPressEvent(e)

        if e.key() == Qt.Key_Z:
            z = int(self.zValue()) + 1
            self.publish(ItemEvent.zChanged, z)

        elif e.key() == Qt.Key_X:
            z = int(self.zValue() - 1)
            self.publish(ItemEvent.zChanged, z)

        elif e.key() == Qt.Key_V:
            self.publish(ItemEvent.vFlipChanged)

        elif e.key() == Qt.Key_H:
            self.publish(ItemEvent.hFlipChanged)

        elif e.key() == Qt.Key_A:
            self.setOffset(-1, 0)

        elif e.key() == Qt.Key_D:
            self.setOffset(1, 0)

        elif e.key() == Qt.Key_W:
            self.setOffset(0, -1)

        elif e.key() == Qt.Key_S:
            self.setOffset(0, 1)

        elif e.key() == Qt.Key_T:
            self.publish(ItemEvent.enableHint)

        elif e.key() == Qt.Key_O:
            self._overlay.enabled = not self._overlay.enabled

        super().keyPressEvent(e)

    def keyReleaseEvent(self, e: QKeyEvent) -> None:
        if e.isAutoRepeat():
            return super().keyReleaseEvent(e)

        if e.key() == Qt.Key_T:
            self.publish(ItemEvent.disableHint)

        super().keyReleaseEvent(e)

    def setOffset(self, x: float, y: float) -> None:
        self.setX(self.x() + x)
        self.setY(self.y() + y)

    def contextMenuEvent(self, e: QGraphicsSceneContextMenuEvent) -> None:
        if self.isSelected():
            menu = ItemMenuDelegate(self, e.screenPos())
            menu.exec()

    def isCentered(self) -> bool:
        return self.sceneBoundingRect().center() == QPointF(0, 0)

    def boundingRect(self) -> QRectF:
        return super().boundingRect().adjusted(0.5, 0.5, -0.5, -0.5)

    def shape(self) -> QPainterPath:
        return self._outline

    def setZValue(self, z: float) -> None:
        super().setZValue(z)
        self._overlay.setZValue(z)

    def itemChange(
        self, change: QGraphicsItem.GraphicsItemChange, value: typing.Any
    ) -> typing.Any:
        if change == QGraphicsItem.ItemPositionChange and self.scene():
            self._overlay.setPos(value.x(), value.y())
            self.publish(ItemEvent.posChanged, value.x(), value.y())

        return value

    def flipChanged(self) -> None:
        self._overlay.setTransform(self.transform())

    def paint(
        self,
        painter: QPainter,
        option,
        widget: QWidget = None,
    ) -> None:
        painter.setRenderHint(QPainter.SmoothPixmapTransform, False)
        painter.drawPixmap(QPoint(), self.pixmap())

        if self.isSelected():
            color = QColor(0, 255, 255, 200)
            pen = QPen(color, 0, Qt.SolidLine, Qt.SquareCap)
            painter.setPen(pen)
            painter.drawRect(self.boundingRect())
