from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QListWidget,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from ..widget import CustomGraphicScene, CustomGraphicSceneOptions
from .spritepaletteview import SpritePaletteView


class SpritePaletteUi:
    def setupUi(self, parent: QWidget):
        parent.setStyleSheet(
            """SpritePaletteWidget > QPushButton {max-width: 16; max-height: 16}"""
        )

        self.spritePalScene = CustomGraphicScene(
            options=CustomGraphicSceneOptions(300, 300, 16, False)
        )
        self.spritePalView = SpritePaletteView(self.spritePalScene)
        self.spritesheetList = QListWidget(parent)

        self.addBtn = QPushButton("+", parent)
        self.addBtn.setFixedSize(16, 16)
        self.addBtn.setToolTip("Add Spritesheets")
        self.delBtn = QPushButton("-", parent)
        self.delBtn.setFixedSize(16, 16)
        self.delBtn.setToolTip("Remove Spritesheet")

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
