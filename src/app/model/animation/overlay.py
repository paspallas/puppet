import typing

from PyQt5.QtCore import QLineF, QRectF, Qt
from PyQt5.QtGui import QColor, QPainter, QPainterPath, QPen
from PyQt5.QtWidgets import QGraphicsItem, QWidget


class Overlay(QGraphicsItem):
    """An overlay for sprite items"""

    def __init__(self, rect: QRectF, outline: QPainterPath):
        super().__init__()

        self.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.setAcceptedMouseButtons(Qt.NoButton)

        self.enabled = False

        self._rect = rect
        self._outline = outline
        self._anchors: typing.List[QLineF] = []
        self.computeBoundingAnchors()

    def computeBoundingAnchors(self) -> None:
        tl = self._rect.topLeft()
        tr = self._rect.topRight()
        bl = self._rect.bottomLeft()
        br = self._rect.bottomRight()

        length = 4

        self._anchors.clear()
        self._anchors.append(QLineF(tl.x(), tl.y(), tl.x() + length, tl.y()))
        self._anchors.append(QLineF(tl.x(), tl.y(), tl.x(), tl.y() + length))
        self._anchors.append(QLineF(tr.x() - length, tr.y(), tr.x(), tr.y()))
        self._anchors.append(QLineF(tr.x(), tr.y(), tr.x(), tr.y() + length))
        self._anchors.append(QLineF(bl.x(), bl.y(), bl.x() + length, bl.y()))
        self._anchors.append(QLineF(bl.x(), bl.y(), bl.x(), bl.y() - length))
        self._anchors.append(QLineF(br.x() - length, br.y(), br.x(), br.y()))
        self._anchors.append(QLineF(br.x(), br.y(), br.x(), br.y() - length))

    def setZValue(self, z: float) -> None:
        super().setZValue(z + 5000)

    def boundingRect(self) -> QRectF:
        return self._rect

    def paint(self, painter: QPainter, option, widget: QWidget) -> None:
        if self.enabled:
            painter.setRenderHint(QPainter.Antialiasing)

            color = QColor(255, 0, 255, 255)
            pen = QPen(color, 0, Qt.SolidLine, Qt.SquareCap)
            painter.setPen(pen)

            painter.drawPath(self._outline)
            painter.drawLines(*self._anchors)

            color.setAlpha(100)
            pen.setColor(color)
            painter.setPen(pen)

            painter.drawRect(self._rect)
