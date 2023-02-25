import typing

import grid
from PyQt5.QtCore import QRectF, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QColor, QFontMetrics, QPainter, QPen
from PyQt5.QtWidgets import (
    QGraphicsDropShadowEffect,
    QGraphicsItem,
    QGraphicsObject,
    QGraphicsSceneMouseEvent,
    QStyleOptionGraphicsItem,
    QWidget,
)

__height__ = 40
__textColor__ = QColor(240, 240, 240)
__hilightColor__ = QColor(Qt.cyan)
__markerColor__ = QColor(200, 200, 200)
__tickOffset__ = 5
__smallTick__ = 5
__bigTick__ = 15


class TimeScale(QGraphicsObject):
    sigSetPlayHeadPosition = pyqtSignal(float)

    def __init__(self, width: float) -> None:
        super().__init__()

        self._rect = QRectF(0, 0, width, __height__)
        self.setZValue(9999)
        self.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.setFlag(QGraphicsItem.ItemIsMovable, False)

        fx = QGraphicsDropShadowEffect()
        self.setGraphicsEffect(fx)
        fx.setXOffset(0)
        fx.setYOffset(2)
        fx.setColor(QColor(60, 60, 60, 60))
        fx.setBlurRadius(4)

        self._playPos = grid.__xoffset__ + __tickOffset__

    def boundingRect(self) -> QRectF:
        return self._rect

    def mousePressEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        if e.buttons() & Qt.LeftButton:
            self.sigSetPlayHeadPosition.emit(e.scenePos().x())

    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget
    ) -> None:
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        pen = QPen(__markerColor__, 0, Qt.SolidLine)
        pen.setCosmetic(True)

        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.black)
        painter.drawRect(self._rect)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)

        fm = self.scene().views()[0].viewport().fontMetrics()

        for x in range(0, int(self._rect.width()), grid.__pxPerFrame__):
            posx = x + grid.__xoffset__ + __tickOffset__

            if x % (grid.__pxPerFrame__ * __tickOffset__) == 0:
                label = f"{x // grid.__pxPerFrame__}f"

                # center the text in the time mark
                r = QRectF(fm.boundingRect(label).translated(posx, 0))
                r.translate(-r.width() / 2, r.height())

                if self._playPos == posx:
                    pen.setColor(__hilightColor__)
                else:
                    pen.setColor(__textColor__)

                painter.setPen(pen)
                painter.drawText(r, label)
                painter.drawLine(posx, __height__ - __bigTick__, posx, __height__)

            else:
                if self._playPos == posx:
                    pen.setColor(__hilightColor__)
                else:
                    pen.setColor(__markerColor__)
                painter.setPen(pen)
                painter.drawLine(posx, __height__ - __smallTick__, posx, __height__)

    @pyqtSlot(float)
    def onAnimationLengthChanged(self, length: float) -> None:
        self._rect.setWidth(length)

    @pyqtSlot(float)
    def onPlayHeadPositionChanged(self, value: float) -> None:
        if self._playPos != value:
            self._playPos = value
            self.update()

    @pyqtSlot(int)
    def onVerticalScrollBarChange(self, scroll: int) -> None:
        self.setY(scroll)
