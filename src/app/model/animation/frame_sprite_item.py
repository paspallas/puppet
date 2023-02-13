import typing
from enum import IntEnum

from PyQt5.QtCore import QPoint, Qt, QVariant, pyqtSlot
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
from .overlay import Overlay


class ItemEvent(IntEnum):
    posChanged = 0
    offsetChanged = 1
    zChanged = 2
    vFlipChanged = 3
    hFlipChanged = 4
    alphaChanged = 5


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

        # make the item selectable regardless of transparency level
        self._outline = Image.outline(pixmap)

        # render the overlay in the correct position
        self._adj = 0.5
        self._overlay = Overlay(
            self.boundingRect().adjusted(self._adj, self._adj, -self._adj, -self._adj),
            self._outline,
        )

    def addedToScene(self):
        self.scene().addItem(self._overlay)
        self._overlay.setZValue(self.zValue())

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
        elif e.key() == Qt.Key_T:
            self.publish(ItemEvent.alphaChanged)
        elif e.key() == Qt.Key_Space:
            self._overlay.enabled = not self._overlay.enabled
            if e.modifiers() & Qt.Modifier.CTRL:
                pass
        else:
            super().keyPressEvent(e)

    # def contextMenuEvent(self, e: QGraphicsSceneContextMenuEvent) -> None:
    #     if self.isSelected():
    #         menu = QMenu("sprite")
    #         remove_action = menu.addAction("remove")
    #         menu.exec_(e.screenPos())

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
        elif change == QGraphicsItem.ItemSelectedChange and self.scene():
            self._overlay.selected = value

        return super().itemChange(change, value)

    def flipChanged(self) -> None:
        """Apply the transformation to the overlay"""
        self._overlay.setTransform(self.transform())

    def aboutToBeRemoved(self) -> None:
        self.scene().removeItem(self._overlay)

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
            color = QColor(255, 0, 255, 100)
            pen = QPen(color, 0, Qt.SolidLine, Qt.SquareCap)
            painter.setPen(pen)
            painter.drawRect(
                self.boundingRect().adjusted(
                    self._adj, self._adj, -self._adj, -self._adj
                )
            )
