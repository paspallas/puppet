import typing

from PyQt5.QtCore import QRectF, Qt, QPoint, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QColor, QFontMetrics, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import (
    QGraphicsItem,
    QGraphicsObject,
    QGraphicsSceneMouseEvent,
    QStyleOptionGraphicsItem,
    QWidget,
)

from ..grid import __midFrame__, __pxPerFrame__, __xoffset__

__rectColor__ = QColor("#2A2A2A")
__textColor__ = QColor("#7C7C7C")

__tickOffset__ = 10 - __pxPerFrame__ // 2
__labelPerFrame__ = 10
__labelPosition__ = __pxPerFrame__ * __labelPerFrame__

__height__ = 30
__tickHeight__ = 4
__textY__ = 3


class TimeScaleItem(QGraphicsObject):
    sigSetPlayHeadPosition = pyqtSignal(float)
    sigClickedTimeScale = pyqtSignal()

    def __init__(self, width: float, fm: QFontMetrics) -> None:
        super().__init__()

        self._rect = QRectF(0, 0, width, __height__)
        self.setZValue(9999)
        self.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.setFlag(QGraphicsItem.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.ItemIgnoresTransformations)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)

        self._clicked = False

        self._fm = fm
        self._pen = QPen(__textColor__, 0, Qt.SolidLine)
        self._pen.setCosmetic(True)

        self._cachedPixmap: QPixMap = None
        self._resetCachedPixmap()

    def _resetCachedPixmap(self) -> None:
        length = self._rect.toRect().width()

        self._cachedPixmap = QPixmap(length, __height__)
        self._cachedPixmap.fill(__rectColor__)

        start = __tickOffset__ + __xoffset__

        with QPainter(self._cachedPixmap) as p:
            p.setRenderHint(QPainter.TextAntialiasing)
            p.setPen(self._pen)

            for x in range(start, length, __pxPerFrame__):
                p.drawLine(x, __height__ - __tickHeight__, x, __height__ - 1)

                if (x - start) % __labelPosition__ == 0:
                    label = str((x - start) // __pxPerFrame__)
                    r = QRectF(self._fm.boundingRect(label).translated(x, __textY__))
                    r.translate(-r.width() / 2, r.height())
                    p.drawText(r, label)

    @property
    def clicked(self) -> bool:
        return self._clicked

    @clicked.setter
    def clicked(self, value: bool) -> None:
        self._clicked = value

    def boundingRect(self) -> QRectF:
        return self._rect

    def mousePressEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        if e.button() == Qt.LeftButton:
            self._clicked = True
            self.sigSetPlayHeadPosition.emit(e.scenePos().x())

    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget
    ) -> None:
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        painter.drawPixmap(QPoint(), self._cachedPixmap)

    @pyqtSlot(float)
    def onAnimationLengthChanged(self, length: float) -> None:
        self._rect.setWidth(length)
        self._resetLabelCache()

    @pyqtSlot(int)
    def onVerticalScrollBarChange(self, scroll: int) -> None:
        self.setY(scroll)
