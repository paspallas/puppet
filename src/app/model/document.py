from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QGraphicsItem

from .animation import AnimationList, AnimationListModel, AnimationModel
from .animation_frame import AnimationFrame, AnimationFrameModel
from .spritesheet import Sprite, SpriteSheetCollectionModel


# TODO used by the spritesheets
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


class Document(QObject):
    sigSpritesChanged = pyqtSignal()
    sigSpriteSheetsChanged = pyqtSignal()

    sigSpriteAddedToCollection = pyqtSignal(QGraphicsItem)

    def __init__(self):
        super().__init__()

        self._animationsListModel = AnimationListModel()
        self._currentAnimationModel = AnimationModel()

        # we only allow a single list of animations per document
        self._animationList = AnimationList()
        self._animationsListModel.setDataSource(self._animationList)

        # allow access to the child classess
        self._spriteSheets = SpriteSheetCollectionModel()
        self._sprites = SpriteCollectionModel()

        #! test the model from the document
        self._currentEditableFrame = AnimationFrame()
        self._currentFrameModel = AnimationFrameModel()
        self._currentFrameModel.setDataSource(self._currentEditableFrame)

        self._forward()

    def frameModel(self) -> AnimationFrameModel:
        return self._currentFrameModel

    def spriteSheets(self) -> SpriteSheetCollectionModel:
        return self._spriteSheets

    def sprites(self) -> SpriteCollectionModel:
        return self._sprites

    def _forward(self):
        self._sprites.spriteAddedToCollection.connect(self.sigSpriteAddedToCollection)

    def addSprite(self, sprite: Sprite) -> None:
        self._sprites.add(sprite)

    def animationListModel(self) -> AnimationListModel:
        return self._animationsListModel

    def animationModel(self) -> AnimationModel:
        return self._currentAnimationModel

    def animationList(self) -> AnimationList:
        return self._animationList
