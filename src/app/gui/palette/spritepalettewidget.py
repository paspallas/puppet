from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget

from ...controller import SpritePaletteController, SpriteGroupController
from ...model.sprite import Sprite
from ...model.spritegroup import SpriteGroupCollectionModel
from ...model.spritesheet import SpriteSheet, SpriteSheetCollectionModel
from .spritepaletteui import SpritePaletteUi


class SpritePaletteWidget(QWidget):

    sigSelectedSpriteChanged = pyqtSignal(Sprite)

    def __init__(self, *args, model: SpriteSheetCollectionModel, **kwargs):
        super().__init__(*args, **kwargs)

        self._ui = SpritePaletteUi()
        self._ui.setupUi(self)

        # internal model for visualizing spritesheets in the scene
        self._groupModel = SpriteGroupCollectionModel()
        self._groupController = SpriteGroupController(self._groupModel)

        self._model = model
        self._controller = SpritePaletteController(self._model)

        self._exposeInternalSignals()
        self._makeConnections()

    def _exposeInternalSignals(self):
        self._ui.spritePalView.sigSelectedSpriteChanged.connect(
            self.sigSelectedSpriteChanged
        )

    def _makeConnections(self):
        self._ui.addBtn.clicked.connect(self._controller.addSpriteSheet)
        self._ui.delBtn.clicked.connect(
            lambda: self._controller.delSpriteSheet(
                self._ui.spritesheetList.currentItem().text()
            )
        )

        self._ui.spritesheetList.currentRowChanged.connect(self.__onCurrentRowChanged)

        self._model.sigSpriteSheetAdded.connect(self.onAddSheet)
        self._model.sigSpriteSheetRemoved.connect(self.onDelSheet)

        # internal sprite group visualization
        self._groupModel.sigGroupAdded.connect(self._ui.spritePalScene.addSprites)

    @pyqtSlot(SpriteSheet)
    def onAddSheet(self, sheet: SpriteSheet) -> None:
        self._groupController.addGroup(sheet)

        row = self._ui.spritesheetList.currentRow()
        self._ui.spritesheetList.addItem(sheet.name)
        self._ui.spritesheetList.setCurrentRow(row + 1)

    @pyqtSlot()
    def onDelSheet(self) -> None:
        row = self._ui.spritesheetList.currentRow()
        item = self._ui.spritesheetList.currentItem()
        if item:
            self._groupController.delGroup(item.text())
            self._ui.spritesheetList.takeItem(row)

    def __onCurrentRowChanged(self, row: int) -> None:
        item = self._ui.spritesheetList.item(row)
        if item:
            self._groupController.showGroup(item.text())
