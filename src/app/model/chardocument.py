from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QGraphicsItem

from .sprite import Sprite
from .spritesheet import SpriteSheetCollectionModel


class SpriteHandler(QObject):
    def __init__(self):
        super().__init__()


class SpriteCollectionModel(QObject):

    spriteAddedToCollection = pyqtSignal(QGraphicsItem)

    def __init__(self):
        super().__init__()

        # keyframes should only store sprite transformations
        # self._sprites: dict[str, Sprite] = dict()
        self._sprites = []

    def add(self, sprite: Sprite) -> None:
        # self._sprites[id] = sprite
        self._sprites.append(sprite)
        self.spriteAddedToCollection.emit(sprite)


class CharDocument(QObject):

    sigSpritesChanged = pyqtSignal()
    sigSpriteSheetsChanged = pyqtSignal()
    sigSpritesChanged = pyqtSignal()

    sigSpriteAddedToCollection = pyqtSignal(QGraphicsItem)

    def __init__(self):
        super().__init__()

        # allow access to the child classess
        self._spriteSheets = SpriteSheetCollectionModel()
        self._sprites = SpriteCollectionModel()

        self._forward()

    def spriteSheets(self) -> SpriteSheetCollectionModel:
        return self._spriteSheets

    def sprites(self) -> SpriteCollectionModel:
        return self._sprites

    def _forward(self):
        self._sprites.spriteAddedToCollection.connect(self.sigSpriteAddedToCollection)

    #! Expose internal public methods of the different components
    # TODO use some metaprogramming to avoid having to manually bind the methods
    def addSprite(self, sprite: Sprite) -> None:
        self._sprites.add(sprite)
