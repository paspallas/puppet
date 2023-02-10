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
from PyQt5.QtGui import QColor, QBrush, QPainter, QWheelEvent


class KeyFrame(QGraphicsObject):
    __selectedColor__ = QColor(Qt.cyan)
    __normalColor__ = QColor(Qt.red)

    def __init__(self, x: float, y: float, w: float, h: float) -> None:
        super().__init__()

        self._rect = QRectF(0, 0, w, h)
        self.setX(x)
        self.setY(y)

        flags = (
            QGraphicsItem.ItemIsSelectable
            | QGraphicsItem.ItemIsMovable
            | QGraphicsItem.ItemSendsGeometryChanges
            | QGraphicsItem.ItemSendsScenePositionChanges
        )

        self.setFlags(flags)
        self.setAcceptHoverEvents(True)

    def boundingRect(self) -> QRectF:
        return self._rect

    def insideControlPoints(self, x: float) -> bool:
        delta = 2.0

        return (
            self.scenePos().x() - delta <= x <= self.scenePos().x() + delta
            or self.scenePos().x() + self._rect.width() - delta
            <= x
            <= self.scenePos().x() + self._rect.width() + delta
        )

    def itemChange(
        self, change: QGraphicsItem.GraphicsItemChange, value: typing.Any
    ) -> typing.Any:
        if change == QGraphicsItem.ItemPositionChange and self.scene():
            return QPointF(value.x(), self.pos().y())

        return super().itemChange(change, value)

    def hoverMoveEvent(self, e: QGraphicsSceneHoverEvent) -> None:
        if self.insideControlPoints(e.scenePos().x()):
            self.setCursor(Qt.SizeHorCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

        super().hoverMoveEvent(e)

    def mouseMoveEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        # print(f"event pos: {e.scenePos().x()}")
        if (
            e.scenePos().x() == self.pos().x()
            or e.scenePos().x() == self.pos().x() + self._rect.width()
        ):
            pass

        super().mouseMoveEvent(e)

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
        super().__init__(0, 0, 1024, 200)

    def addKeyFrame(self, key: KeyFrame) -> None:
        self.addItem(key)


class TimeLineView(QGraphicsView):
    def __init__(self, scene: QGraphicsScene, parent) -> None:
        super().__init__(scene, parent)

        self.setMouseTracking(True)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scalings = 0

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
