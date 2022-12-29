from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QFrame, QGraphicsView, QSizePolicy, QWidget

from app.gui.control.pancontrol import PanControl
from app.gui.control.zoomcontrol import ZoomControl
from app.model.sprite import Sprite

from .graphicscene import GraphicScene


class GraphicView(QGraphicsView):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        PanControl(self)
        ZoomControl(self)

        self._scene = GraphicScene(self)
        self._setup()

    def _setup(self) -> None:
        self.setScene(self._scene)
        self.setFrameStyle(QFrame.NoFrame)
        self.setContentsMargins(0, 0, 0, 0)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMouseTracking(True)
