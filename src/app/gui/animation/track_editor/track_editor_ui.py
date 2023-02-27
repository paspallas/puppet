import typing

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QPushButton,
    QTreeView,
    QVBoxLayout,
    QWidget,
)

from ....resources import resources


class TrackEditorUi:
    def setupUi(self, parent: QWidget) -> None:
        self.trackTree = QTreeView()
        self.trackTree.setHeaderHidden(True)
        self.trackTree.setMouseTracking(True)
        self.trackTree.setUniformRowHeights(True)
        self.trackTree.setAlternatingRowColors(True)

        self.animCombo = QComboBox()
        self.animCombo.setFixedWidth(120)
        self.newAnimBtn = QPushButton(QIcon(":/icon/16/add.png"), "")
        self.delAnimBtn = QPushButton(QIcon(":/icon/16/delete.png"), "")
        self.newAnimBtn.setToolTip("Create a new animation")
        self.delAnimBtn.setToolTip("Delete the current animation")

        hbox = QHBoxLayout()
        hbox.addWidget(self.animCombo)
        hbox.addStretch()
        hbox.addWidget(self.newAnimBtn)
        hbox.addWidget(self.delAnimBtn)

        vbox = QVBoxLayout(parent)
        vbox.addLayout(hbox)
        vbox.addWidget(self.trackTree)
