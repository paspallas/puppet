import typing

from PyQt5.QtCore import QLineF, QRectF, Qt
from PyQt5.QtGui import QColor, QPainter, QPen

__pxPerFrame__ = 10
__trackHeight__ = 20
__xoffset__ = 50
__yoffset__ = 60
__color__ = QColor(30, 30, 30)

__lines__: typing.List[QLineF] = []


class Grid:
    @staticmethod
    def computeGrid(rect: QRectF) -> None:
        __lines__.clear()

        left = int(rect.left() - (rect.left() % __pxPerFrame__)) + __xoffset__
        right = int(rect.right())
        top = int(rect.top() - rect.top() % __trackHeight__) + __yoffset__
        bottom = int(rect.bottom())

        for x in range(left, right, __pxPerFrame__):
            __lines__.append(QLineF(x, top, x, bottom))

        for y in range(top, bottom + 1, __trackHeight__):
            __lines__.append(QLineF(0, y, right, y))

    @staticmethod
    def paint(painter: QPainter) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(__color__, 0, Qt.SolidLine, Qt.SquareCap)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLines(*__lines__)

    @staticmethod
    def alignTo(x: float, offset: float = 0) -> float:
        pos = round(x / __pxPerFrame__) * __pxPerFrame__
        if pos < __xoffset__:
            pos = __xoffset__

        return pos + offset
