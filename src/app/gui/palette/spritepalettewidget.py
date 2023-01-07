from pathlib import Path

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QBoxLayout,
    QDockWidget,
    QHBoxLayout,
    QListWidget,
    QSplitter,
    QToolBar,
    QVBoxLayout,
    QWidget,
)
from spriteutil.spritesheet import SpriteSheet

from app.model.sprite import Sprite, SpriteGroup

from ..dialog import OpenImageDialog
from .spritepalettescene import SpritePaletteScene
from .spritepaletteview import SpritePaletteView


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

        splitter = QSplitter(Qt.Horizontal, self)
        splitter.addWidget(self._ui_spritesheetList)
        splitter.addWidget(self._ui_spritePalView)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)

        content = QHBoxLayout()
        content.addWidget(splitter)
        box.addLayout(content)

    def _forwardSignals(self):
        self._ui_spritePalView.sigSelectedSpriteChanged.connect(
            self.sigSelectedSpriteChanged
        )

    def _makeConnections(self):
        self._ui_spritesheetList.itemClicked.connect(
            lambda item: self._ui_spritePalScene.showLayer(item.text())
        )

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
