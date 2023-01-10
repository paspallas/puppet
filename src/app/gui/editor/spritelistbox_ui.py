from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class SpriteListBoxUi:
    def setupUi(self, parent: QWidget):
        parent.setMaximumSize(QSize(250, 300))
        parent.setStyleSheet(
            """SpriteListBox > QPushButton {max-width: 32; max-height: 32}"""
        )

        self.list = QListWidget(parent)
        self.list.setDragDropMode(QAbstractItemView.InternalMove)

        self.upBtn = QPushButton("+")
        self.upBtn.setFixedSize(16, 16)
        self.downBtn = QPushButton("-")
        self.downBtn.setFixedSize(16, 16)

        btnBox = QHBoxLayout()
        btnBox.addWidget(self.upBtn, 0, Qt.AlignLeft)
        btnBox.addWidget(self.downBtn, 0, Qt.AlignLeft)
        btnBox.addStretch()

        vbox = QVBoxLayout(parent)
        vbox.addWidget(self.list)
        vbox.addLayout(btnBox)
