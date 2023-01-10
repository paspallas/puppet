from PyQt5.QtCore import QPoint, QRectF, Qt, pyqtSlot
from PyQt5.QtGui import QBrush, QColor, QMouseEvent, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QGraphicsScene, QWidget

from ...model.sprite import Sprite


class SpritePaletteScene(QGraphicsScene):
    def __init__(self, *args, width: int = 300, height: int = 300, **kwargs):
        super().__init__(*args, **kwargs)

        self.setSceneRect(-width / 2, -height / 2, width, height)

    @pyqtSlot(list)
    def addSprites(self, sprites: list[Sprite]) -> None:
        for sprite in sprites:
            self.addItem(sprite)

    @pyqtSlot(list)
    def delSprites(self, sprites: list[Sprite]) -> None:
        for sprite in sprites:
            self.removeItem(sprite)

    def drawBackground(self, painter: QPainter, rect: QRectF) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.NoPen))

        # draw checkerboard pattern
        SQUARE_SIZE = 16

        left = int(rect.left() - rect.left() % SQUARE_SIZE)
        top = int(rect.top() - rect.top() % SQUARE_SIZE)

        for y in range(top, int(rect.bottom()), SQUARE_SIZE):
            for x in range(left, int(rect.right()), SQUARE_SIZE):
                is_dark = (x / SQUARE_SIZE + y / SQUARE_SIZE) % 2

                color = QColor("#505050") if is_dark else QColor("#767676")
                painter.fillRect(QRectF(x, y, SQUARE_SIZE, SQUARE_SIZE), QBrush(color))
