from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsScene, QWidget

from app.model.sprite import Sprite


class GraphicScene(QGraphicsScene):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self._setup()

    def _setup(self) -> None:
        self.setBackgroundBrush(QColor("#41444D"))

        # add some test sprites
        self._sprite1 = Sprite("F:/devel/kai-mag/test/yoko.png")
        self._sprite2 = Sprite("F:/devel/kai-mag/test/leg.png")
        self._sprite3 = Sprite("F:/devel/kai-mag/test/upper_leg.png")

        self.addItem(self._sprite1)
        self.addItem(self._sprite2)
        self.addItem(self._sprite3)

        # self.setSceneRect(0, 0, self.width(), self.height())
