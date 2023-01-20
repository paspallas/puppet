import typing
from enum import IntEnum

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent, QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsSceneMouseEvent, QGraphicsItem

from ...util.pubsub import Publisher


class ItemEvent(IntEnum):
    xChanged = 0
    yChanged = 1
    zChanged = 2


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
            # TODO we have to check how many items there are in the collection!

            z = self.zValue() + 1
            self.setZValue(z)

            self.publish(ItemEvent.zChanged, z)

        elif e.key() == Qt.Key_W:
            z = self.zValue() - 1
            self.setZValue(z)

            self.publish(ItemEvent.zChanged, z)

        super().keyPressEvent(e)
