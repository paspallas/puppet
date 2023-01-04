from PyQt5.QtCore import QLineF, QRectF, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QBrush, QColor, QKeyEvent, QPainter, QPen, QTransform
from PyQt5.QtWidgets import (
    QGraphicsItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsSceneMouseEvent,
    QPushButton,
    QWidget,
)

from app.model.bone import Bone
from app.model.sprite import Sprite


class GraphicScene(QGraphicsScene):
    def __init__(self, parent: QWidget, width: float = 640.0, height: float = 480.0):
        super().__init__(parent)

        self.setSceneRect(-width / 2.0, -height / 2.0, width, height)

    @pyqtSlot(Sprite)
    def addSprite(self, sprite: Sprite):
        self.addItem(sprite)

    def keyPressEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key.Key_Backspace:
            e.accept()

            items = self.selectedItems()

            for item in items:
                self.removeItem(item)
        else:
            super().keyPressEvent(e)

    def drawBackground(self, painter: QPainter, rect: QRectF) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.NoPen))

        # draw checkerboard pattern
        SQUARE_SIZE = 32

        left = int(rect.left() - rect.left() % SQUARE_SIZE)
        top = int(rect.top() - rect.top() % SQUARE_SIZE)

        for y in range(top, int(rect.bottom()), SQUARE_SIZE):
            for x in range(left, int(rect.right()), SQUARE_SIZE):
                is_dark = (x / SQUARE_SIZE + y / SQUARE_SIZE) % 2

                color = QColor("#505050") if is_dark else QColor("#767676")
                painter.fillRect(QRectF(x, y, SQUARE_SIZE, SQUARE_SIZE), QBrush(color))

        # l = rect.left()
        # r = rect.right()
        # t = rect.top()
        # b = rect.bottom()

        # # center visual indicator
        # lines = [QLineF(l, 0, r, 0), QLineF(0, t, 0, b)]

        # pen = QPen(QColor("#202020"), 0, Qt.DashLine)
        # pen.setCosmetic(True)
        # painter.setPen(pen)

        # painter.drawLines(*lines)
