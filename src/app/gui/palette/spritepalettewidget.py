from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QListWidget,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from ...model.sprite import Sprite, SpriteGroup
from ...model.spritesheet import SpriteSheet, SpriteSheetCollection
from ..dialog import OpenImageDialog
from .spritepalettescene import SpritePaletteScene
from .spritepaletteview import SpritePaletteView


class SpritePaletteWidget(QWidget):

    sigSelectedSpriteChanged = pyqtSignal(Sprite)

    def __init__(self, *args, model: SpriteSheetCollection, **kwargs):
        super().__init__(*args, **kwargs)

        self._model: SpriteSheetCollection = model

        self._setupUi()
        self._forwardSignals()
        self._makeConnections()

    def setModel(self, model: SpriteSheetCollection) -> None:
        self._model = model

    def _setupUi(self):
        self.setStyleSheet(
            """SpritePaletteWidget > QPushButton {max-width: 16; max-height: 16}"""
        )

        self._ui_spritePalScene = SpritePaletteScene()
        self._ui_spritePalView = SpritePaletteView(self._ui_spritePalScene)
        self._ui_spritesheetList = QListWidget(self)

        self._ui_addBtn = QPushButton("+")
        self._ui_addBtn.setFixedSize(16, 16)
        self._ui_addBtn.setToolTip("Add Spritesheets")
        self._ui_delBtn = QPushButton("-")
        self._ui_delBtn.setFixedSize(16, 16)
        self._ui_delBtn.setToolTip("Remove Spritesheet")

        splitter = QSplitter(Qt.Horizontal, self)
        splitter.addWidget(self._ui_spritesheetList)
        splitter.addWidget(self._ui_spritePalView)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)

        btnBox = QVBoxLayout()
        btnBox.setDirection(QVBoxLayout.TopToBottom)
        btnBox.addWidget(self._ui_addBtn, 0, Qt.AlignTop)
        btnBox.addWidget(self._ui_delBtn, 0, Qt.AlignTop)
        btnBox.addStretch()

        content = QHBoxLayout(self)
        content.addLayout(btnBox)
        content.addWidget(splitter)

    def _forwardSignals(self):
        self._ui_spritePalView.sigSelectedSpriteChanged.connect(
            self.sigSelectedSpriteChanged
        )

    def _makeConnections(self):
        self._ui_addBtn.clicked.connect(self._addSheet)
        self._ui_delBtn.clicked.connect(self._delSheet)
        self._ui_spritesheetList.currentRowChanged.connect(self._selectedSheetChanged)

        # model to view
        self._model.sigSpriteSheetAdded.connect(self.sltOnAddSheet)

    @pyqtSlot(SpriteSheet)
    def sltOnAddSheet(self, sheet: SpriteSheet) -> None:
        self._ui_spritePalScene.addSpriteSheet(sheet)

        row = self._ui_spritesheetList.currentRow()
        self._ui_spritesheetList.addItem(sheet.name)
        self._ui_spritesheetList.setCurrentRow(row + 1)

    @pyqtSlot(int)
    def _selectedSheetChanged(self, row: int) -> None:
        item = self._ui_spritesheetList.item(row)

        if item:
            self._ui_spritePalScene.showLayer(item.text())

    @pyqtSlot()
    def _delSheet(self) -> None:
        row = self._ui_spritesheetList.currentRow()
        item = self._ui_spritesheetList.item(row)
        if item:
            self._model.delSpriteSheet(item.text())
            self._ui_spritePalScene.delSpriteSheet(item.text())
            self._ui_spritesheetList.takeItem(row)

    @pyqtSlot()
    def _addSheet(self) -> None:
        dialog = OpenImageDialog(
            self, "Add Spritesheets", "", "Sprite Sheet Images (*.png)"
        )
        if dialog.exec() == OpenImageDialog.Accepted:
            for path in dialog.getFilesSelected():
                self._model.addSpriteSheet(path)
