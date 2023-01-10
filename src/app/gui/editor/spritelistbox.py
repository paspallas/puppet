from PyQt5.QtCore import QPoint, QRectF, QSize, QSizeF, Qt, pyqtSlot
from PyQt5.QtGui import QColor, QPainter, QPaintEvent
from PyQt5.QtWidgets import QWidget

from ...model.sprite import Sprite, SpriteObject
from .spritelistbox_ui import SpriteListBoxUi


class SpriteListBox(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self._ui = SpriteListBoxUi()
        self._ui.setupUi(self)

        self._makeConnections()

    def _makeConnections(self) -> None:
        self._ui.list.model().rowsMoved.connect(self._reorder)
        self._ui.upBtn.clicked.connect(self._moveSpriteUp)
        self._ui.downBtn.clicked.connect(self._moveSpriteDown)

    @pyqtSlot()
    def _moveSpriteUp(self) -> None:
        row = self._list.currentRow()
        if row - 1 >= 0:
            self._swapItems(row, row - 1)

    @pyqtSlot()
    def _moveSpriteDown(self) -> None:
        row = self._list.currentRow()
        if row + 1 <= self._list.count() - 1:
            self._swapItems(row, row + 1)

    def _swapItems(self, row_1: int, row_2: int) -> None:
        # taking the item modifies the number of rows
        # get the second item first
        item2 = self._list.item(row_2)
        item1 = self._list.takeItem(row_1)

        self._list.insertItem(row_2, item1)
        self._list.setCurrentItem(item1)

    def _reorder(self) -> None:
        pass

    def paintEvent(self, e: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QColor("#424242"))
        painter.setBrush(QColor("#353535"))
        rect = QRectF(
            QPoint(), QSizeF(self.size() - 0.5 * painter.pen().width() * QSize(1, 1))
        )
        painter.drawRoundedRect(rect, 4, 4)
