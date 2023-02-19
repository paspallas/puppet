from enum import IntEnum
import typing

from PyQt5.QtCore import Qt, QRectF, QPointF, QPoint, pyqtSignal
from PyQt5.QtWidgets import (
    QGraphicsView,
    QGraphicsScene,
    QGraphicsItem,
    QGraphicsRectItem,
    QGraphicsObject,
    QGraphicsDropShadowEffect,
    QStyleOptionGraphicsItem,
    QWidget,
    QGraphicsSceneMouseEvent,
    QGraphicsSceneHoverEvent,
)
from PyQt5.QtGui import QColor, QBrush, QPainter, QPen, QWheelEvent


from key_frame_item import KeyFrameItem


class TimeLineScene(QGraphicsScene):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(0, 0, 2000, 200)

    def addKeyFrame(self, key: KeyFrameItem) -> None:
        self.addItem(key)


class TimeLineView(QGraphicsView):
    def __init__(self, scene: QGraphicsScene, parent) -> None:
        super().__init__(scene, parent)

        self.setMouseTracking(True)
        self.setContentsMargins(10, 10, 10, 10)

        self.setRenderHint(QPainter.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.centerOn(0, 0)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.scalings = 0

    def drawBackground(self, painter: QPainter, rect: QRectF) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(QColor(30, 30, 30), 0, Qt.SolidLine, Qt.SquareCap)
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
    from qtmodern import styles
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
            key_1 = KeyFrameItem(10, 60, 10, 20)
            key_2 = KeyFrameItem(160, 60, 150, 20)
            key_2.sigTrackDurationChanged.connect(self.trackDuration)

            self.scene.addKeyFrame(key_1)
            self.scene.addKeyFrame(key_2)

        def trackDuration(self, value: float) -> None:
            print(f"track {value // 10} frames long")

    app = QApplication([])
    styles.dark(app)
    w = Window()
    sys.exit(app.exec_())
