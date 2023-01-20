import typing
from enum import Enum

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsSceneMouseEvent

from ...util.pubsub import Publisher


class ItemEvent(Enum):
    xChanged = 0
    yChanged = 1
    zChanged = 2


class FrameSpriteItem(QGraphicsPixmapItem, Publisher):
    """A graphicsitem used for visualization and user interaction in the editor scene"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def mousePressEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        super().mouseMoveEvent(e)

    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.key() == Qt.Key.Key_Q:
            z = self.zValue() + 1
            self.setZValue(z)

            self.publish(ItemEvent.zChanged, z)

        elif e.key() == Qt.Key_W:
            z = self.zValue() - 1
            self.setZValue(z)

            self.publish(ItemEvent.zChanged, z)

        super().keyPressEvent(e)
