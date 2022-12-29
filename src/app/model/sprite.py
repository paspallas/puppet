from PyQt5.QtGui import QColor, QPixmap
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
