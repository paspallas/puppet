from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSlider,
    QTableView,
    QTreeView,
    QVBoxLayout,
    QWidget,
)

import src.app.resources.resources


class SpriteListBoxUi:
    def setupUi(self, parent: QWidget):
        parent.setStyleSheet(
            """SpriteListBox > QPushButton {max-width: 16; max-height: 16}"""
        )

        self.opacitySlide = QSlider()
        self.opacitySlide.setRange(0, 100)
        self.opacitySlide.setValue(100)
        self.opacitySlide.setTickInterval(1)
        self.opacitySlide.setOrientation(Qt.Horizontal)
        self.opacityLbl = QLabel("Opacity: ")
        self.opacityLbl.setBuddy(self.opacitySlide)

        self.flipVerticalChk = QCheckBox("Flip Vertical")
        self.flipHorizontalChk = QCheckBox("Flip Horizontal")

        h1 = QHBoxLayout()
        h1.addWidget(self.opacityLbl, stretch=1)
        h1.addWidget(self.opacitySlide, stretch=3)

        h2 = QHBoxLayout()
        h2.addWidget(self.flipHorizontalChk)
        h2.addWidget(self.flipVerticalChk)

        vbox = QVBoxLayout(parent)
        vbox.addLayout(h1)
        vbox.addLayout(h2)

        self.list = QTreeView(parent)
        self.list.setRootIsDecorated(False)
        self.list.setDragEnabled(True)
        self.list.setAcceptDrops(True)
        self.list.setDragDropOverwriteMode(False)
        self.list.setDragDropMode(QAbstractItemView.DragDrop)
        self.list.setDropIndicatorShown(True)
        self.list.setDefaultDropAction(Qt.MoveAction)
        self.list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.list.header().setStretchLastSection(False)

        self.upBtn = QPushButton(QIcon(":/icon/16/up.png"), "")
        self.downBtn = QPushButton(QIcon(":/icon/16/down.png"), "")
        self.delBtn = QPushButton(QIcon(":/icon/16/delete.png"), "")

        btnBox = QHBoxLayout()
        btnBox.addWidget(self.upBtn, 0, Qt.AlignLeft)
        btnBox.addWidget(self.downBtn, 0, Qt.AlignLeft)
        btnBox.addStretch()
        btnBox.addWidget(self.delBtn, 0, Qt.AlignRight)

        vbox.addWidget(self.list)
        vbox.addLayout(btnBox)
