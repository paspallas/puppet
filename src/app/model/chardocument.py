from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal

from .animation import AnimationCollectionModel
from .sprite import Sprite
from .spritesheet import SpriteSheetCollectionModel


class SpriteCollectionModel(QObject):
    def __init__(self):
        super().__init__()

        # keyframes should only store sprite transformations
        self._sprites: dict[str, Sprite] = dict()

    def add(self, id: str, sprite: Sprite) -> None:
        self._sprites[id] = sprite


class CharDocument(QObject):
    """Represents the currently edited character"""

    sigSpritesChanged = pyqtSignal()
    sigSpriteSheetsChanged = pyqtSignal()
    sigSpritesChanged = pyqtSignal()

    def __init__(self):
        super().__init__()

        # allow access to the child classess
        self.animations = AnimationCollectionModel()
        self.spriteSheets = SpriteSheetCollectionModel()
        self.sprites = SpriteCollectionModel()
