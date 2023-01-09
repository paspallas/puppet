from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget

from ...controller import SpritePaletteController
from ...model.sprite import Sprite
from ...model.spritegroup import SpriteGroup
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
        self._controller = SpritePaletteController(self._model)

        self._exposeInternalSignals()
        self._makeConnections()

    def _exposeInternalSignals(self):
        self._ui.spritePalView.sigSelectedSpriteChanged.connect(
            self.sigSelectedSpriteChanged
        )

    def _makeConnections(self):
        self._ui.addBtn.clicked.connect(self._openSheetDialog)
        self._ui.delBtn.clicked.connect(
            lambda: self._controller.delSpriteSheet(
                self._ui.spritesheetList.currentItem().text()
            )
        )
        self._ui.spritesheetList.currentRowChanged.connect(self._selectedSheetChanged)

        self._model.sigSpriteSheetAdded.connect(self.onAddSheet)
        self._model.sigSpriteSheetRemoved.connect(self.onDelSheet)

    @pyqtSlot(SpriteSheet)
    def onAddSheet(self, sheet: SpriteSheet) -> None:
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
    def onDelSheet(self) -> None:
        row = self._ui.spritesheetList.currentRow()
        item = self._ui.spritesheetList.currentItem()
        if item:
            self._ui.spritePalScene.delSpriteSheet(item.text())
            self._ui.spritesheetList.takeItem(row)

    @pyqtSlot()
    def _openSheetDialog(self) -> None:
        dialog = OpenImageDialog(
            self, "Add Spritesheets", "", "Sprite Sheet Images (*.png)"
        )
        if dialog.exec() == OpenImageDialog.Accepted:
            self._controller.addSpriteSheet(dialog.getFilesSelected())
