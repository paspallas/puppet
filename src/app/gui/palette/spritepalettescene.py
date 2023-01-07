from PyQt5.QtCore import QPoint, QRectF, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QBrush, QColor, QMouseEvent, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QGraphicsScene, QWidget

from app.model.sprite import Sprite, SpriteGroup


class SpritePaletteScene(QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setSceneRect(10, -10, 300, 300)
        self._ui_backgroundColor = QBrush(QColor("#404040"))

        self._sprite_sheets = dict()

    def addSpriteSheet(self, name: str, sprites: [Sprite]):
        self.hideAll()

        group = SpriteGroup()
        for sprite in sprites:
            sprite.setPos(sprite.x, sprite.y)
            sprite.lock()
            self.addItem(sprite)
            group.add(sprite)
        group.show()

        self._sprite_sheets[name] = group

    @pyqtSlot()
    def showLayer(self, name: str):
        self.hideAll()
        self._sprite_sheets[name].show()

    def hideAll(self):
        for group in self._sprite_sheets.values():
            group.hide()

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
