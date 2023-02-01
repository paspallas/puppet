from typing import NamedTuple

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QMouseEvent, QPainter, QResizeEvent, QSurfaceFormat
from PyQt5.QtWidgets import (
    QFrame,
    QGraphicsItem,
    QGraphicsView,
    QOpenGLWidget,
    QSizePolicy,
)

from ..viewcontrol import PanControl, ZoomControl


class CustomGraphicViewOptions(NamedTuple):
    drag: bool
    scroll_bar: bool
    center_on_resize: bool


class CustomGraphicView(QGraphicsView):
    def __init__(self, *args, options: CustomGraphicViewOptions, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._activeItem = None

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
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setMouseTracking(True)

        ZoomControl(self)
        PanControl(self)

    def resizeEvent(self, e: QResizeEvent) -> None:
        if not self._centerOnResize:
            super().resizeEvent(e)
            return

        self.centerOn(0, 0)
        super().resizeEvent(e)

    def setOpenglViewport(self) -> None:
        fmt = QSurfaceFormat()
        fmt.setSamples(2)
        gl = QOpenGLWidget()
        gl.setFormat(fmt)
        self.setViewport(gl)
        self.setRenderHints(
            QPainter.Antialiasing
            | QPainter.TextAntialiasing
            | QPainter.SmoothPixmapTransform
        )
