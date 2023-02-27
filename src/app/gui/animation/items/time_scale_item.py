import typing

from PyQt5.QtCore import QRectF, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QColor, QFontMetrics, QPainter, QPen
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

__height__ = 30
__tickOffset__ = 10
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

        self._clicked = False

        self._fm = fm
        self._pen = QPen(__textColor__, 0, Qt.SolidLine)
        self._pen.setCosmetic(True)

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
        painter.setRenderHints(QPainter.TextAntialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(__rectColor__)
        painter.drawRect(self._rect)

        painter.setPen(self._pen)
        painter.setBrush(Qt.NoBrush)

        max_ = int(self._rect.width())
        for x in range(0, max_, __pxPerFrame__):
            posx = x + __xoffset__ + __tickOffset__ - __midFrame__

            if x % (__pxPerFrame__ * __tickOffset__) == 0:
                label = f"{x // __pxPerFrame__}"

                r = QRectF(self._fm.boundingRect(label).translated(posx, __textY__))
                r.translate(-r.width() / 2, r.height())
                painter.drawText(r, label)

            if posx <= max_:
                painter.drawLine(
                    posx, __height__ - __tickHeight__, posx, __height__ - 1
                )

    @pyqtSlot(float)
    def onAnimationLengthChanged(self, length: float) -> None:
        self._rect.setWidth(length)

    @pyqtSlot(int)
    def onVerticalScrollBarChange(self, scroll: int) -> None:
        self.setY(scroll)
