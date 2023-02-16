from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QListWidget,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from ...resources import resources
from ..viewcontrol import PanControl, ZoomControl
from ..widget import (
    CustomGraphicScene,
    CustomGraphicView,
    CustomGraphicViewOptions,
)


class SpritePaletteUi:
    def setupUi(self, parent: QWidget):
        self.spritePalScene = CustomGraphicScene(200, 200, parent)
        self.spritePalView = CustomGraphicView(
            self.spritePalScene,
            parent,
            options=CustomGraphicViewOptions(False, False, 16, False),
        )

        PanControl(self.spritePalView)
        ZoomControl(self.spritePalView)

        # sprites view
        sprBox = QVBoxLayout()
        sprBox.addWidget(self.spritePalView)
        spritesGroup = QGroupBox("Sprites")
        spritesGroup.setLayout(sprBox)

        # spritesheets listbox
        self.spritesheetList = QListWidget(parent)
        self.addBtn = QPushButton(QIcon(":/icon/16/add.png"), "", parent)
        self.addBtn.setToolTip("Add spritesheets")
        self.delBtn = QPushButton(QIcon(":/icon/16/delete.png"), "", parent)
        self.delBtn.setToolTip("Delete selected spritesheet")

        btnBox = QHBoxLayout()
        btnBox.addStretch()
        btnBox.addWidget(self.addBtn, 0, Qt.AlignRight)
        btnBox.addWidget(self.delBtn, 0, Qt.AlignRight)

        vbox = QVBoxLayout()
        vbox.addLayout(btnBox)
        vbox.addWidget(self.spritesheetList)

        sheetsGroup = QGroupBox("Sprite Sheets")
        sheetsGroup.setLayout(vbox)

        splitter = QSplitter(Qt.Horizontal, parent)
        splitter.addWidget(sheetsGroup)
        splitter.addWidget(spritesGroup)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)

        content = QHBoxLayout(parent)
        content.addWidget(splitter)
