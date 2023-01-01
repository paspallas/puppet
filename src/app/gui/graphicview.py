from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QFrame, QGraphicsView, QSizePolicy, QWidget

from app.model.sprite import Sprite

from .graphicscene import GraphicScene
from .navcontrol import PanControl, ZoomControl


class GraphicView(QGraphicsView):
    def __init__(self, parent: QWidget, scene: GraphicScene):
        super().__init__(scene, parent)

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
