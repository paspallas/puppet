from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QGraphicsItem

from ..gui.dialog import OpenImageDialog
from ..model.sprite import Sprite
from ..model.spritesheet import SpriteSheetCollectionModel


class SpritePaletteController(QObject):
    def __init__(self, model: SpriteSheetCollectionModel):
        super().__init__()

        self._model = model

    @pyqtSlot()
    def addSpriteSheet(self) -> None:
        dialog = OpenImageDialog(
            None, "Add Spritesheets", "", "Sprite Sheet Images (*.png)"
        )
        if dialog.exec() == OpenImageDialog.Accepted:
            paths = dialog.getFilesSelected()
            for path in paths:
                self._model.addSpriteSheet(path)

    @pyqtSlot(str)
    def delSpriteSheet(self, id: str) -> None:
        self._model.delSpriteSheet(id)

    @pyqtSlot(list)
    def selectedSprite(self, sprites: list[Sprite]) -> None:
        # We are only interested in the first item selected
        if len(sprites) > 0:
            clone = sprites[0].copy()
            print(clone)
