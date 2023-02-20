import typing

import grid
from PyQt5.QtCore import QObject, QPointF, QRectF, QSize, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QColor, QFont, QFontMetrics, QPainter, QPen
from PyQt5.QtWidgets import qApp

__height__ = 40
__textColor__ = QColor(240, 240, 240)
__hilightColor__ = QColor(Qt.cyan)
__markerColor__ = QColor(200, 200, 200)
__pxPerFrame__ = 5


class TimeRuler(QObject):
    def __init__(self) -> None:
        super().__init__()

        self._playbackPosition = 0

    def paint(self, painter: QPainter, rect: QRectF, width: float, font: QFont) -> None:
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen(__markerColor__, 0, Qt.SolidLine)
        pen.setCosmetic(True)

        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.black)
        painter.drawRect(QRectF(0, 0, width, __height__))
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.setFont(font)

        fm = QFontMetrics(font)

        for x in range(0, int(width), grid.__width__):
            if x % (grid.__width__ * __pxPerFrame__) == 0:
                if x != 0:
                    label = f"{x // grid.__width__}f"
                    r = QRectF(fm.boundingRect(label).translated(x, 0))

                    # center the text in the time mark
                    r.translate(-r.width() / 2, r.height())

                    if self._playbackPosition == x:
                        pen.setColor(__hilightColor__)
                    else:
                        pen.setColor(__textColor__)
                    painter.setPen(pen)
                    painter.drawText(r, label)

                pen.setColor(__markerColor__)
                painter.setPen(pen)
                painter.drawLine(x, __height__ - 15, x, __height__)

            else:
                painter.drawLine(x, __height__ - 5, x, __height__)

    @pyqtSlot(float)
    def onPlayBackPositionChange(self, value: float) -> None:
        self._playbackPosition = value
