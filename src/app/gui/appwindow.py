from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow

from ..model.animation_frame import AnimationFrame
from ..model.animation_frame_model import AnimationFrameModel
from ..model.animation_frame_sprite import FrameSprite
from ..model.chardocument import CharDocument
from .appwindow_ui import EditModeUi
from .menu.main_menu import MainMenu


class AppWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Puppet Studio")
        self.setMinimumSize(1280, 800)

        self._ui = EditModeUi()
        self._ui.setupUi(self)
        self._menu = MainMenu(self)

        # document models
        self._document = CharDocument()
        # self._spritesheets = SpriteSheetCollectionModel()

        self._animFrame = AnimationFrame()
        # when adding items to the data source the model must be notified to
        # reflect changes
        self._animFrame.add(FrameSprite("Head", 10, 10, False, True, 30))
        self._animFrame.add(FrameSprite("Chest", 10, 10, False, True, 30))
        self._animFrame.add(FrameSprite("Foot", 10, 10, False, True, 30))
        self._animFrame.add(FrameSprite("hand", 10, 10, False, True, 30))
        self._animFrame.add(FrameSprite("Head", 10, 10, False, True, 30))
        self._animFrame.add(FrameSprite("Chest", 10, 10, False, True, 30))
        self._animFrame.add(FrameSprite("Foot", 10, 10, False, True, 30))
        self._animFrame.add(FrameSprite("hand", 10, 10, False, True, 30))

        self._animFrameModel = AnimationFrameModel()
        self._animFrameModel.setDataSource(self._animFrame)

        #! test passing the model to the main editor
        self._ui.charEditor.setModel(self._animFrameModel)

        # TODO clean this up
        self._ui.charEditor.setDocument(self._document)
        self._ui.spritePaletteDock.setModel(self._document)
