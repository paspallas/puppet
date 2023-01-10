from typing import NamedTuple

from PyQt5.QtCore import QPoint, QRectF, QLineF, Qt, pyqtSlot
from PyQt5.QtGui import QBrush, QColor, QMouseEvent, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsScene, QWidget


CustomGraphicSceneOptions = NamedTuple(
    "CustomGraphicSceneOptions", width=int, height=int, grid_size=int, show_center=bool
)


class CustomGraphicScene(QGraphicsScene):
    def __init__(self, *args, options: CustomGraphicSceneOptions, **kwargs):
        super().__init__(*args, **kwargs)

        self._showCenterGrid = options.show_center
        self._gridSize = options.grid_size
        self.setSceneRect(
            -options.width / 2, -options.height / 2, options.width, options.height
        )

    @pyqtSlot(list)
    def addItems(self, items: list[QGraphicsItem]) -> None:
        for item in items:
            self.addItem(item)

    @pyqtSlot(list)
    def delItems(self, items: list[QGraphicsItem]) -> None:
        for item in items:
            self.removeItem(item)

    def drawBackground(self, painter: QPainter, rect: QRectF) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.NoPen))

        left = int(rect.left() - rect.left() % self._gridSize)
        top = int(rect.top() - rect.top() % self._gridSize)

        for y in range(top, int(rect.bottom()), self._gridSize):
            for x in range(left, int(rect.right()), self._gridSize):
                is_dark = (x / self._gridSize + y / self._gridSize) % 2

                color = QColor("#505050") if is_dark else QColor("#767676")
                painter.fillRect(
                    QRectF(x, y, self._gridSize, self._gridSize), QBrush(color)
                )

        if self._showCenterGrid:
            l = rect.left()
            r = rect.right()
            t = rect.top()
            b = rect.bottom()

            # center visual indicator
            lines = [QLineF(l, 0, r, 0), QLineF(0, t, 0, b)]

            pen = QPen(QColor("#202020"), 0, Qt.DashLine)
            pen.setCosmetic(True)
            painter.setPen(pen)
            painter.drawLines(*lines)