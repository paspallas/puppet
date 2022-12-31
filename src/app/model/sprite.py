from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QBrush, QColor, QPainter, QPixmap
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPixmapItem, QWidget

DEFAULT_ALPHA_MASK = "#FF00FF"


class Sprite(QGraphicsPixmapItem):
    def __init__(self, path: str, parent: QWidget = None):
        super().__init__(parent=parent)

        self._pixmap = None

        self._setItemFlags()

        self._setPixmapFromFile(path)
        self.setAlphaMask()

        self.setPixmap(self._pixmap)

        self.setOpacity(50.0)
        self.setTintColor(QColor(255, 0, 0, 100))

    def _setItemFlags(self):
        flags = (
            QGraphicsItem.ItemIsSelectable
            | QGraphicsItem.ItemIsMovable
            | QGraphicsItem.ItemIsFocusable
            | QGraphicsItem.ItemSendsScenePositionChanges
        )

        self.setFlags(flags)
        self.setAcceptHoverEvents(True)

    def _setPixmapFromFile(self, path: str):
        self._pixmap = QPixmap(path)

    def _setPixmapFromSpriteSheet(self):
        pass

    def setAlphaMask(self):
        self._pixmap.setMask(
            self._pixmap.createMaskFromColor(QColor(DEFAULT_ALPHA_MASK))
        )

    def setOpacity(self, opacity: float) -> None:
        if 0 <= opacity <= 100.0:
            transparent = QPixmap(self._pixmap.size())
            transparent.fill(Qt.transparent)

            painter = QPainter(transparent)
            painter.setOpacity(opacity * 0.01)
            painter.drawPixmap(QPoint(), self._pixmap)
            painter.end()

            self._pixmap = transparent
            self.setPixmap(self._pixmap)

    def setTintColor(self, color: QColor) -> None:
        painter = QPainter(self._pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceAtop)
        painter.fillRect(self._pixmap.rect(), color)
        painter.end()

        self.setPixmap(self._pixmap)
