from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QDockWidget, QWidget, QGraphicsItem

from ...controller import SpritePaletteController, SpriteGroupController
from ...model.sprite import Sprite
from ...model.spritegroup import SpriteGroupCollectionModel
from ...model.spritesheet import SpriteSheet, SpriteSheetCollectionModel
from ...model.chardocument import CharDocument
from .spritepalette_ui import SpritePaletteUi


class SpritePaletteDock(QDockWidget):

    sigSelectedSprite = pyqtSignal(QGraphicsItem)

    def __init__(self, *args, model: CharDocument, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Sprite Palette")
        self.setAllowedAreas(Qt.BottomDockWidgetArea)

        self._container = QWidget(self)
        self.setWidget(self._container)

        self._ui = SpritePaletteUi()
        self._ui.setupUi(self._container)

        # internal model for visualizing spritesheets in the scene
        self._groupModel = SpriteGroupCollectionModel()
        self._groupController = SpriteGroupController(self._groupModel)

        # should route internal signals slots in the document to it's components?
        self._model = model.spriteSheets()
        self._controller = SpritePaletteController(model)

        self._exposeInternalSignals()
        self._makeConnections()

    def setModel(self, model) -> None:
        self._model = model

    def _exposeInternalSignals(self):
        self._ui.spritePalView.sigSelectedItem.connect(self.sigSelectedSprite)

    def _makeConnections(self):
        self._ui.addBtn.clicked.connect(self._controller.addSpriteSheet)
        self._ui.delBtn.clicked.connect(
            lambda: self._controller.delSpriteSheet(
                self._ui.spritesheetList.currentItem().text()
            )
        )

        self._ui.spritesheetList.currentRowChanged.connect(self.__onCurrentRowChanged)
        self._ui.spritePalView.sigSelectedItem.connect(self._controller.selectedSprite)

        # subscribe to model signals
        self._model.sigSpriteSheetAdded.connect(self.onAddSheet)
        self._model.sigSpriteSheetRemoved.connect(self.onDelSheet)

        # internal sprite group visualization
        self._groupModel.sigGroupAdded.connect(self._ui.spritePalScene.addItems)
        self._groupModel.sigGroupDeleted.connect(self._ui.spritePalScene.delItems)

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
