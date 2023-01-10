from typing import NamedTuple

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QFrame, QGraphicsItem, QGraphicsView

from ..viewcontrol import PanControl, ZoomControl

CustomGraphicViewOptions = NamedTuple(
    "CustomGraphicViewOptions", drag=bool, scroll_bar=bool
)


class CustomGraphicView(QGraphicsView):

    sigSelectedSpriteChanged = pyqtSignal(QGraphicsItem)

    def __init__(self, *args, options: CustomGraphicViewOptions, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFrameStyle(QFrame.NoFrame)
        self.setContentsMargins(0, 0, 0, 0)

        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOn if options.scroll_bar else Qt.ScrollBarAlwaysOff
        )
        self.setVerticalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff if options.scroll_bar else Qt.ScrollBarAlwaysOff
        )

        self.setDragMode(
            QGraphicsView.RubberBandDrag if options.drag else QGraphicsView.NoDrag
        )

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setMouseTracking(True)

        ZoomControl(self)
        PanControl(self)
