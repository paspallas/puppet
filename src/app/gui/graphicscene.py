from PyQt5.QtCore import Qt, QLineF, QRectF, pyqtSlot
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen, QTransform
from PyQt5.QtWidgets import (
    QGraphicsItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QWidget,
    QPushButton,
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

    def drawBackground(self, painter: QPainter, rect: QRectF) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(rect, QBrush(QColor("#505050")))

        # checkerboard pattern
        # SIZE = 32

        # for y in range(0, int(rect.height() / SIZE)):
        #     ty = y * SIZE + rect.top()

        #     for x in range(0, int(rect.width() / SIZE)):
        #         tx = x * SIZE + rect.left()

        #         color = QColor("#505050") if (x + y) % 2 else QColor("#767676")
        #         painter.fillRect(QRectF(tx, ty, SIZE, SIZE), QBrush(color))

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

    # def dragEnterEvent(self, e: QGraphicsSceneDragDropEvent):
    #     pass
