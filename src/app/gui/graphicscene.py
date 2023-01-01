from PyQt5.QtCore import Qt, QLineF, QRectF
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen, QTransform
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsRectItem, QGraphicsScene, QWidget

from app.model.bone import Bone
from app.model.sprite import Sprite


class GraphicScene(QGraphicsScene):
    def __init__(self, parent: QWidget, width: float = 640.0, height: float = 480.0):
        super().__init__(parent)

        self.setSceneRect(-width / 2.0, -height / 2.0, width, height)
        self._setup()

    def _setup(self) -> None:

        # add some test sprites
        self._sprite1 = Sprite("F:/devel/kai-mag/test/yoko.png")
        self._sprite2 = Sprite("F:/devel/kai-mag/test/leg.png")
        self._sprite3 = Sprite("F:/devel/kai-mag/test/upper_leg.png")
        self._sprite4 = Sprite("F:/devel/kai-mag/test/upper_leg.png")
        self._sprite5 = Sprite("F:/devel/kai-mag/test/hand.png")
        self._sprite6 = Sprite("F:/devel/kai-mag/test/feet.png")

        self.addItem(self._sprite1)
        self.addItem(self._sprite2)
        self.addItem(self._sprite3)
        # self.addItem(self._sprite4)
        # self.addItem(self._sprite5)
        # self.addItem(self._sprite6)

        # self.addItem(Bone())

    # override
    def drawBackground(self, painter: QPainter, rect: QRectF) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(rect, QBrush(QColor("#41444D")))

        l = rect.left()
        r = rect.right()
        t = rect.top()
        b = rect.bottom()

        lines = [QLineF(l, 0, r, 0), QLineF(0, t, 0, b)]

        pen = QPen(QColor("#202020"), 0, Qt.DashLine)
        pen.setCosmetic(True)
        painter.setPen(pen)

        painter.drawLines(*lines)
