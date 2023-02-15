import math
import typing

from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtWidgets import (
    QGraphicsView,
    QGraphicsScene,
    QGraphicsItem,
    QGraphicsRectItem,
    QGraphicsObject,
    QStyleOptionGraphicsItem,
    QWidget,
    QGraphicsSceneMouseEvent,
    QGraphicsSceneHoverEvent,
)
from PyQt5.QtGui import QColor, QBrush, QPainter, QPen, QWheelEvent


class KeyFrame(QGraphicsObject):
    __selectedColor__ = QColor(Qt.cyan)
    __normalColor__ = QColor(Qt.red)

    def __init__(self, x: float, y: float, w: float, h: float) -> None:
        super().__init__()

        self._rect = QRectF(x, y, w, h)
        # self.setX(x)
        # self.setY(y)

        flags = (
            QGraphicsItem.ItemIsSelectable
            | QGraphicsItem.ItemIsMovable
            | QGraphicsItem.ItemSendsGeometryChanges
            | QGraphicsItem.ItemSendsScenePositionChanges
        )

        self.setFlags(flags)
        self.setAcceptHoverEvents(True)

        self._resizeOrigin = 0.0
        self._resize = False
        self._clickRect = None

    def boundingRect(self) -> QRectF:
        return self._rect

    def insideControlPoints(self, x: float) -> bool:
        delta = 2.0

        return (
            self._rect.left() <= x <= self._rect.left() + delta
            or self._rect.right() - delta <= x <= self._rect.right()
        )

    def itemChange(
        self, change: QGraphicsItem.GraphicsItemChange, value: typing.Any
    ) -> typing.Any:
        if change == QGraphicsItem.ItemPositionChange and self.scene():
            return QPointF(value.x(), self.pos().y())

        return super().itemChange(change, value)

    def updateItemSize(self, x: float) -> None:
        self.prepareGeometryChange()

        offset = 5.0
        delta = x - self._resizeOrigin
        print(delta)

        right = self._rect.right()
        left = self._rect.left()

        if right - offset < x < right + offset:
            self._rect = self._clickRect.adjusted(0, 0, delta, 0)
        elif left - offset < x < left + offset:
            self._rect = self._clickRect.adjusted(delta, 0, 0, 0)

    def hoverMoveEvent(self, e: QGraphicsSceneHoverEvent) -> None:
        if self.insideControlPoints(e.pos().x()):
            self.setCursor(Qt.SizeHorCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

        super().hoverMoveEvent(e)

    def mouseMoveEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        if self._resize:
            self.updateItemSize(e.pos().x())

        else:
            super().mouseMoveEvent(e)

    def mousePressEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        if e.buttons() == Qt.LeftButton:
            if self.insideControlPoints(e.pos().x()):
                self._resize = True
                self._resizeOrigin = e.pos().x()
                self._clickRect = self._rect

        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        self._resize = False

        super().mouseReleaseEvent(e)

    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget
    ) -> None:
        painter.setRenderHint(QPainter.Antialiasing)

        if self.isSelected():
            painter.setBrush(self.__selectedColor__)
        else:
            painter.setBrush(self.__normalColor__)

        painter.drawRoundedRect(self._rect, 4, 4)


class TimeLineScene(QGraphicsScene):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(0, 0, 2000, 200)

    def addKeyFrame(self, key: KeyFrame) -> None:
        self.addItem(key)


class TimeLineView(QGraphicsView):
    def __init__(self, scene: QGraphicsScene, parent) -> None:
        super().__init__(scene, parent)

        self.setMouseTracking(True)
        self.setContentsMargins(10, 10, 10, 10)

        self.setRenderHint(QPainter.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.centerOn(0, 0)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scalings = 0

    def drawBackground(self, painter: QPainter, rect: QRectF) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.black, 0, Qt.SolidLine, Qt.SquareCap)
        pen.setCosmetic(True)
        painter.setPen(pen)

        xSize = 10
        ySize = 20

        left = int(rect.left() - rect.left() % xSize)
        top = int(rect.top() - rect.top() % ySize)

        for y in range(top, int(rect.bottom()), ySize):
            for x in range(left, int(rect.right()), xSize):
                painter.drawRect(QRectF(x, y, xSize, ySize))

    def wheelEvent(self, e: QWheelEvent) -> None:
        if e.modifiers() & Qt.Modifier.CTRL:
            degs = e.angleDelta().y() / 8
            steps = degs / 15
            self.scalings += steps

            if self.scalings * steps < 0:
                self.scalings = steps

            factor = 1.0 + (self.scalings / 160.0)
            self.scale(factor, 1.0)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow

    class Window(QMainWindow):
        def __init__(self) -> None:
            super().__init__()

            self.setWindowTitle("Timeline")

            self.scene = TimeLineScene(self)
            self.view = TimeLineView(self.scene, self)

            self.setCentralWidget(self.view)
            self.show()

            self.populate()

        def populate(self) -> None:
            key_1 = KeyFrame(10, 50, 150, 30)
            key_2 = KeyFrame(160, 50, 150, 30)

            self.scene.addKeyFrame(key_1)
            self.scene.addKeyFrame(key_2)

    app = QApplication([])
    w = Window()
    sys.exit(app.exec_())
