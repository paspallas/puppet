import typing

from PyQt5.QtCore import QLineF, QRectF, Qt
from PyQt5.QtGui import QColor, QPainter, QPen

__pxPerFrame__ = 10
__height__ = 20
__xoffset__ = 50
__yoffset__ = 60
__color__ = QColor(30, 30, 30)


class Grid:
    def __init__(self) -> None:
        self._lines = []

    def computeGrid(self, rect: QRectF) -> None:
        self._lines.clear()

        left = int(rect.left() - (rect.left() % __pxPerFrame__)) + __xoffset__
        right = int(rect.right())
        top = int(rect.top() - rect.top() % __height__) + __yoffset__
        bottom = int(rect.bottom())

        for x in range(left, right, __pxPerFrame__):
            self._lines.append(QLineF(x, top, x, bottom))

        for y in range(top, bottom, __height__):
            self._lines.append(QLineF(0, y, right, y))

    def paint(self, painter: QPainter) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(__color__, 0, Qt.SolidLine, Qt.SquareCap)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLines(*self._lines)

    @staticmethod
    def alignTo(x: float, offset: float = 0) -> float:
        pos = round(x / __pxPerFrame__) * __pxPerFrame__
        if pos < __xoffset__:
            pos = __xoffset__

        return pos + offset
