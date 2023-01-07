from PyQt5.QtCore import QPoint, QRectF, QSize, QSizeF, Qt, pyqtSlot
from PyQt5.QtGui import QColor, QPainter, QPaintEvent
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QListWidget,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from app.model.sprite import Sprite, SpriteObject


class SpriteListBox(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self._setupUI()
        self._makeConnections()

        self._list.addItem("head")
        self._list.addItem("legs")
        self._list.addItem("hands")
        self._list.addItem("feet")
        self._list.addItem("body")

    def _setupUI(self) -> None:
        self.setMaximumSize(QSize(250, 300))

        self._list = QListWidget(self)
        self._list.setDragDropMode(QAbstractItemView.InternalMove)
        self._list.model().rowsMoved.connect(self._reorder)

        self._btnUp = QPushButton("+")
        self._btnDown = QPushButton("-")
        self._btnUp.setMaximumSize(QSize(32, 32))
        self._btnDown.setMaximumSize(QSize(32, 32))

        vbox = QVBoxLayout(self)
        vbox.addWidget(self._list)
        btnBox = QHBoxLayout()
        vbox.addLayout(btnBox)
        hspacer = QSpacerItem(64, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        btnBox.addWidget(self._btnUp, 0, Qt.AlignLeft)
        btnBox.addWidget(self._btnDown, 0, Qt.AlignLeft)
        btnBox.addItem(hspacer)

    def _makeConnections(self) -> None:
        self._btnUp.clicked.connect(self._moveSpriteUp)
        self._btnDown.clicked.connect(self._moveSpriteDown)

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

        print(f"swap {item1.text()} with {item2.text()}")

        # TODO call method in frame container to swap z-indexes

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
