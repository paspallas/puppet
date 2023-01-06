from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QMouseEvent, QPainter
from PyQt5.QtWidgets import QFrame, QGraphicsScene, QGraphicsView

from app.model.sprite import Sprite, SpriteGroup

from ...viewcontrol import PanControl, ZoomControl


class SpritePaletteView(QGraphicsView):

    selectedSpriteChanged = pyqtSignal(Sprite)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFrameStyle(QFrame.NoFrame)
        self.setContentsMargins(0, 0, 0, 0)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setMouseTracking(True)

        ZoomControl(self)
        PanControl(self)

    def mousePressEvent(self, e: QMouseEvent):
        selected_sprite = self.itemAt(e.pos())

        if isinstance(selected_sprite, Sprite):
            copy = selected_sprite.copy()
            copy.unlock()

            self.selectedSpriteChanged.emit(copy)

        super().mousePressEvent(e)
