import typing
from enum import IntEnum

from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtGui import QKeyEvent, QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsSceneMouseEvent, QGraphicsItem

from ...util.pubsub import Publisher


class ItemEvent(IntEnum):
    posChanged = 0
    zChanged = 1
    vFlipChanged = 2
    hFlipChanged = 3


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

    def mousePressEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        super().mousePressEvent(e)

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

        super().keyPressEvent(e)

    def itemChange(self, change, value: typing.Any) -> typing.Any:
        if change == QGraphicsItem.ItemPositionChange and self.scene():
            self.publish(ItemEvent.posChanged, value.x(), value.y())

        return super().itemChange(change, value)
