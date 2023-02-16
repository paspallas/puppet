from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QAction, QGraphicsItem, QMenu


class ItemMenuDelegate(QMenu):
    def __init__(self, sprite: QGraphicsItem, pos: QPoint) -> None:
        super().__init__("Sprite")
        self._sprite = sprite
        self._pos = pos

        self.addAction("Center", self._center)

    def exec(self) -> None:
        super().exec_(self._pos)

    def _center(self) -> None:
        self._sprite.setPos(
            -self._sprite.boundingRect().width() // 2,
            -self._sprite.boundingRect().height() // 2,
        )
