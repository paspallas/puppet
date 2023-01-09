from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget

from ...model.sprite import Sprite, SpriteGroup
from ...model.spritesheet import SpriteSheet, SpriteSheetCollection
from ..dialog import OpenImageDialog
from .spritepaletteui import SpritePaletteUi


class SpritePaletteWidget(QWidget):

    sigSelectedSpriteChanged = pyqtSignal(Sprite)

    def __init__(self, *args, model: SpriteSheetCollection, **kwargs):
        super().__init__(*args, **kwargs)

        self._ui = SpritePaletteUi()
        self._ui.setupUi(self)

        self._model: SpriteSheetCollection = model

        self._exposeInternalSignals()
        self._makeConnections()

    def setModel(self, model: SpriteSheetCollection) -> None:
        self._model = model

    def _exposeInternalSignals(self):
        self._ui.spritePalView.sigSelectedSpriteChanged.connect(
            self.sigSelectedSpriteChanged
        )

    def _makeConnections(self):
        self._ui.addBtn.clicked.connect(self._addSheet)
        self._ui.delBtn.clicked.connect(self._delSheet)
        self._ui.spritesheetList.currentRowChanged.connect(self._selectedSheetChanged)

        # model to view
        self._model.sigSpriteSheetAdded.connect(self.sltOnAddSheet)

    @pyqtSlot(SpriteSheet)
    def sltOnAddSheet(self, sheet: SpriteSheet) -> None:
        self._ui.spritePalScene.addSpriteSheet(sheet)

        row = self._ui.spritesheetList.currentRow()
        self._ui.spritesheetList.addItem(sheet.name)
        self._ui.spritesheetList.setCurrentRow(row + 1)

    @pyqtSlot(int)
    def _selectedSheetChanged(self, row: int) -> None:
        item = self._ui.spritesheetList.item(row)

        if item:
            self._ui.spritePalScene.showLayer(item.text())

    @pyqtSlot()
    def _delSheet(self) -> None:
        row = self._ui.spritesheetList.currentRow()
        item = self._ui.spritesheetList.item(row)
        if item:
            self._model.delSpriteSheet(item.text())
            self._ui.spritePalScene.delSpriteSheet(item.text())
            self._ui.spritesheetList.takeItem(row)

    @pyqtSlot()
    def _addSheet(self) -> None:
        dialog = OpenImageDialog(
            self, "Add Spritesheets", "", "Sprite Sheet Images (*.png)"
        )
        if dialog.exec() == OpenImageDialog.Accepted:
            for path in dialog.getFilesSelected():
                self._model.addSpriteSheet(path)
