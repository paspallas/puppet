from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QListWidget,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from ...resources import resources
from ..widget import CustomGraphicScene, CustomGraphicSceneOptions
from ..widget import CustomGraphicView, CustomGraphicViewOptions


class SpritePaletteUi:
    def setupUi(self, parent: QWidget):

        self.spritePalScene = CustomGraphicScene(
            parent=parent, options=CustomGraphicSceneOptions(200, 200, 16, False)
        )

        self.spritePalView = CustomGraphicView(
            self.spritePalScene,
            parent,
            options=CustomGraphicViewOptions(False, False, False),
        )
        self.spritesheetList = QListWidget(parent)

        self.addBtn = QPushButton(QIcon(":/icon/16/add.png"), "", parent)
        self.addBtn.setToolTip("Add Spritesheets")
        self.delBtn = QPushButton(QIcon(":/icon/16/delete.png"), "", parent)
        self.delBtn.setToolTip("Delete Spritesheet")

        splitter = QSplitter(Qt.Horizontal, parent)
        splitter.addWidget(self.spritesheetList)
        splitter.addWidget(self.spritePalView)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)

        btnBox = QVBoxLayout()
        btnBox.setDirection(QVBoxLayout.TopToBottom)
        btnBox.addWidget(self.addBtn, 0, Qt.AlignTop)
        btnBox.addWidget(self.delBtn, 0, Qt.AlignTop)
        btnBox.addStretch()

        content = QHBoxLayout(parent)
        content.addLayout(btnBox)
        content.addWidget(splitter)
