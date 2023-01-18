from PyQt5.QtCore import QPoint, Qt, pyqtSignal
from PyQt5.QtGui import QMouseEvent, QPainter
from PyQt5.QtWidgets import QFrame, QGraphicsItem, QGraphicsView, QSizePolicy, QWidget

from app.model.sprite import Sprite

from ..viewcontrol import PanControl, ZoomControl
from .chareditorscene import CharEditorScene


class CharEditorView(QGraphicsView):
    sigSelectedItemChanged = pyqtSignal(QGraphicsItem)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        PanControl(self)
        ZoomControl(self)

        self._setup()

    def _setup(self) -> None:
        self.setFrameStyle(QFrame.NoFrame)
        self.setContentsMargins(0, 0, 0, 0)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setMouseTracking(True)

    def mousePressEvent(self, e: QMouseEvent):
        selected_sprite = self.itemAt(e.pos())

        if isinstance(selected_sprite, Sprite):
            self.sigSelectedItemChanged.emit(selected_sprite)

        super().mousePressEvent(e)
