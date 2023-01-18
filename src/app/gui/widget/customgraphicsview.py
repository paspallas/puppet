from typing import NamedTuple

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPainter, QResizeEvent
from PyQt5.QtWidgets import (
    QFrame,
    QGraphicsItem,
    QGraphicsSceneMouseEvent,
    QSizePolicy,
    QGraphicsView,
)

from ..viewcontrol import PanControl, ZoomControl

CustomGraphicViewOptions = NamedTuple(
    "CustomGraphicViewOptions", drag=bool, scroll_bar=bool, center_on_resize=bool
)


class CustomGraphicView(QGraphicsView):

    sigSelectedItem = pyqtSignal(QGraphicsItem)

    def __init__(self, *args, options: CustomGraphicViewOptions, **kwargs):
        super().__init__(*args, **kwargs)

        self._centerOnResize = options.center_on_resize

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
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setMouseTracking(True)

        ZoomControl(self)
        PanControl(self)

    def mousePressEvent(self, e: QGraphicsSceneMouseEvent):
        item = self.itemAt(e.pos())
        if item:
            self.sigSelectedItem.emit(item)

    def resizeEvent(self, e: QResizeEvent):
        if not self._centerOnResize:
            super().resizeEvent(e)
            return

        self.centerOn(0, 0)
        e.accept()
