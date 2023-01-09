from PyQt5.QtCore import QObject, pyqtSlot

from ..model.spritesheet import SpriteSheetCollection


class SpritePaletteController(QObject):
    def __init__(self, model: SpriteSheetCollection):
        super().__init__()

        self._model = model

    @pyqtSlot()
    def addSpriteSheet(self, paths: list[str]):
        for path in paths:
            self._model.addSpriteSheet(path)

    @pyqtSlot(str)
    def delSpriteSheet(self, name: str):
        self._model.delSpriteSheet(name)
