from PyQt5.QtCore import QPoint, QRectF, Qt
from PyQt5.QtGui import QBrush, QColor, QPainter, QPainterPath, QPen
from PyQt5.QtWidgets import QGraphicsItem, QWidget


class Bone(QGraphicsItem):
    def __init__(self):
        super().__init__()

        self._length = 0
        self._setItemFlags()

    def setLength(self, lenght: int) -> None:
        self._length = length

    def _setItemFlags(self):
        flags = (
            QGraphicsItem.ItemIsSelectable
            | QGraphicsItem.ItemIsMovable
            | QGraphicsItem.ItemIsFocusable
            | QGraphicsItem.ItemSendsScenePositionChanges
        )

        self.setFlags(flags)
        self.setAcceptHoverEvents(True)

    def paint(self, painter: QPainter, option, widget: QWidget = None) -> None:
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen(QColor(Qt.transparent), 0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        brush = QBrush(QColor(70, 70, 70, 255))

        painter.setPen(pen)
        painter.setBrush(brush)

        painter.drawPath(self.shape())

    def boundingRect(self) -> QRectF:
        return self.shape().boundingRect()

    def shape(self) -> QPainterPath:
        # starting circle
        # path.addEllipse(QRectF(x0-radius, y0-radius, 2*radius, 2*radius))

        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)

        path.addEllipse(10, 10, 32, 32)
        path.moveTo(10 + 32, 10 + 16)
        path.lineTo(10 + 16, 100)
        path.lineTo(10, 10 + 16)
        path.closeSubpath()

        return path.simplified()
