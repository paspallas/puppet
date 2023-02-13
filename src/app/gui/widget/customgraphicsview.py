from typing import NamedTuple

from PyQt5.QtCore import QLineF, QPointF, QRectF, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen, QResizeEvent, QWheelEvent
from PyQt5.QtWidgets import (
    QFrame,
    QGraphicsItem,
    QGraphicsView,
    QSizePolicy,
    QStyleOptionGraphicsItem,
)


class CustomGraphicViewOptions(NamedTuple):
    drag: bool
    scroll_bar: bool
    grid_size: int
    show_center: bool


class CustomGraphicView(QGraphicsView):
    zoomChanged = pyqtSignal(float)

    def __init__(self, *args, options: CustomGraphicViewOptions, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._showCenterGrid = options.show_center
        self._gridSize = options.grid_size

        self.setFrameStyle(QFrame.NoFrame)
        self.setContentsMargins(0, 0, 0, 0)

        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOn if options.scroll_bar else Qt.ScrollBarAlwaysOff
        )
        self.setVerticalScrollBarPolicy(
            Qt.ScrollBarAlwaysOn if options.scroll_bar else Qt.ScrollBarAlwaysOff
        )

        self.setDragMode(
            QGraphicsView.RubberBandDrag if options.drag else QGraphicsView.NoDrag
        )

        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.centerOn(0, 0)

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setRenderHints(QPainter.Antialiasing)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMouseTracking(True)

    def wheelEvent(self, e: QWheelEvent) -> None:
        if e.modifiers() & Qt.Modifier.ALT:
            h = self.horizontalScrollBar()
            h.setValue(h.value() + e.angleDelta().x() // 8)
            e.accept()
        elif e.modifiers() & Qt.Modifier.CTRL:
            v = self.verticalScrollBar()
            v.setValue(v.value() - e.angleDelta().y() // 8)
            e.accept()

    def fitInView(self, item: QGraphicsItem) -> None:
        super().fitInView(item, Qt.KeepAspectRatio)
        self.zoomChanged.emit(
            QStyleOptionGraphicsItem.levelOfDetailFromTransform(self.transform())
        )

    def drawBackground(self, painter: QPainter, rect: QRectF) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.NoPen))

        left = int(rect.left() - rect.left() % self._gridSize)
        top = int(rect.top() - rect.top() % self._gridSize)

        for y in range(top, int(rect.bottom()), self._gridSize):
            for x in range(left, int(rect.right()), self._gridSize):
                is_dark = (x / self._gridSize + y / self._gridSize) % 2

                color = QColor("#505050") if is_dark else QColor("#767676")
                painter.fillRect(
                    QRectF(x, y, self._gridSize, self._gridSize), QBrush(color)
                )

        if self._showCenterGrid:
            l = rect.left()
            r = rect.right()
            t = rect.top()
            b = rect.bottom()

            # center visual indicator
            lines = [QLineF(l, 0, r, 0), QLineF(0, t, 0, b)]

            pen = QPen(QColor("#080808"), 0, Qt.SolidLine)
            pen.setCosmetic(True)
            painter.setPen(pen)
            painter.drawLines(*lines)
            painter.drawRect(QRectF(-160, -112, 320, 224))

    def drawForeground(self, painter: QPainter, rect: QRectF) -> None:
        if not self._showCenterGrid:
            return

        start = 6
        end = 2

        lines = [
            QLineF(-start, 0, -end, 0),
            QLineF(0, -start, 0, -end),
            QLineF(end, 0, start, 0),
            QLineF(0, start, 0, end),
        ]

        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(QColor(210, 210, 210, 200), 2, Qt.SolidLine)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLines(*lines)
        painter.drawEllipse(QPointF(0, 0), 1, 1)
