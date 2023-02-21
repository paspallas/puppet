from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QPushButton,
    QTreeView,
    QVBoxLayout,
    QWidget,
)

from ...resources import resources


class SpriteListBoxUi:
    def setupUi(self, parent: QWidget) -> None:
        self.list = QTreeView(parent)
        self.list.setMouseTracking(True)
        self.list.setWordWrap(True)
        self.list.setStyleSheet("QTreeView::item:hover{background-color:#4A91D9;}")
        self.list.setRootIsDecorated(False)
        self.list.setDragEnabled(True)
        self.list.setUniformRowHeights(True)
        self.list.setAcceptDrops(True)
        self.list.setDragDropOverwriteMode(False)
        self.list.setDragDropMode(QAbstractItemView.DragDrop)
        self.list.setDropIndicatorShown(True)
        self.list.setDefaultDropAction(Qt.MoveAction)
        self.list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.list.setHeaderHidden(True)
        self.list.header().setStretchLastSection(False)

        self.upBtn = QPushButton(QIcon(":/icon/16/up.png"), "")
        self.upBtn.setToolTip("Move sprite up")
        self.downBtn = QPushButton(QIcon(":/icon/16/down.png"), "")
        self.downBtn.setToolTip("Move sprite down")
        self.delBtn = QPushButton(QIcon(":/icon/16/delete.png"), "")
        self.delBtn.setToolTip("Delete selected sprite")
        self.copyBtn = QPushButton(QIcon(":/icon/16/copy.png"), "")
        self.copyBtn.setToolTip("Copy selected sprite")

        btnBox = QHBoxLayout()
        btnBox.addWidget(self.upBtn, 0, Qt.AlignLeft)
        btnBox.addWidget(self.downBtn, 0, Qt.AlignLeft)
        btnBox.addStretch()
        btnBox.addWidget(self.copyBtn, 0, Qt.AlignRight)
        btnBox.addWidget(self.delBtn, 0, Qt.AlignRight)

        spriteListLay = QVBoxLayout()
        spriteListLay.addWidget(self.list)
        spriteListLay.addLayout(btnBox)

        self.spriteListBox = QGroupBox("Sprite Order", parent)
        self.spriteListBox.setLayout(spriteListLay)

        layout = QVBoxLayout(parent)
        layout.addWidget(self.spriteListBox)

    def updateHeaders(self) -> None:
        """Update header size policy after the model has been set"""
        self.list.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.list.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.list.header().setSectionResizeMode(2, QHeaderView.ResizeToContents)
