from pathlib import Path

from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QBoxLayout,
    QDockWidget,
    QHBoxLayout,
    QListWidget,
    QToolBar,
    QVBoxLayout,
    QWidget,
)
from spriteutil.spritesheet import SpriteSheet

from app.model.sprite import Sprite, SpriteGroup

from .spritepalettescene import SpritePaletteScene
from .spritepaletteview import SpritePaletteView
from ...dialog import OpenImageDialog


class SpritePaletteWidget(QWidget):

    sigSelectedSpriteChanged = pyqtSignal(Sprite)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._setupUi()
        self._forwardSignals()
        self._makeConnections()

    def _setupUi(self):
        self._ui_spritePalScene = SpritePaletteScene()
        self._ui_spritePalView = SpritePaletteView(self._ui_spritePalScene)
        self._ui_spritesheetList = QListWidget(self)

        self._toolbar = QToolBar()
        self._toolbar.setOrientation(Qt.Vertical)
        self._toolbar.addAction("+", self._addSpriteSheet)

        box = QBoxLayout(QBoxLayout.LeftToRight, self)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(self._toolbar)

        content = QHBoxLayout()
        content.addWidget(self._ui_spritesheetList, stretch=1)
        content.addWidget(self._ui_spritePalView, stretch=2)
        box.addLayout(content)

    def _forwardSignals(self):
        """Expose signals of the private widgets"""
        self._ui_spritePalView.sigSelectedSpriteChanged.connect(
            self.sigSelectedSpriteChanged
        )

    def _makeConnections(self):
        self._ui_spritesheetList.itemClicked.connect(
            lambda item: self._ui_spritePalScene.showLayer(item.text())
        )

    @pyqtSlot(Sprite)
    def onSelectedSpriteChanged(self, sprite: Sprite):
        self.selectedSpriteChanged.emit(sprite)

    @pyqtSlot()
    def _addSpriteSheet(self) -> None:
        dialog = OpenImageDialog(self, "Load Spritesheets", "", "Sprite Sheet (*.png)")
        if dialog.exec() == OpenImageDialog.Accepted:
            for path in dialog.getFilesSelected():
                name = Path(path).stem
                self._ui_spritesheetList.addItem(name)

                sheet = SpriteSheet(path)
                sprites, _ = sheet.find_sprites()

                sprite_sheet = QPixmap(path)
                layer = [
                    Sprite.fromSpriteSheet(
                        *sprite.top_left, sprite.width, sprite.height, sprite_sheet
                    )
                    for sprite in sprites
                ]

                self._ui_spritePalScene.addSpriteSheet(name, layer)


class SpritePaletteDock(QDockWidget):

    sigSelectedSpriteChanged = pyqtSignal(Sprite)

    def __init__(self, parent: QWidget = None):
        super().__init__("Sprite Palette", parent)

        self._ui_spritePaletteWid = SpritePaletteWidget(self)
        self.setWidget(self._ui_spritePaletteWid)
        self._forwardSignals()

    @pyqtSlot(Sprite)
    def onSelectedSpriteChanged(self, sprite: Sprite):
        self._ui_spritePaletteWid.onSelectedSpriteChanged(sprite)

    def _forwardSignals(self):
        self._ui_spritePaletteWid.sigSelectedSpriteChanged.connect(
            self.sigSelectedSpriteChanged
        )
