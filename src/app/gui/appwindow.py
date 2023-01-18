from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QAction, QMainWindow, QMenu

from ..model.animation_frame import AnimationFrame
from ..model.animation_frame_model import AnimationFrameModel
from ..model.animation_frame_sprite import FrameSprite
from ..model.chardocument import CharDocument
from .appwindow_ui import EditModeUi


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Puppet Studio")
        self.setMinimumSize(1280, 800)

        self._ui = EditModeUi()
        self._ui.setupUi(self)

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

        self._setupMenu()

    def _fullScreen(self):
        if self.windowState() & Qt.WindowMaximized:
            self.setWindowState(Qt.WindowFullScreen)
        else:
            self.setWindowState(Qt.WindowMaximized)

    def _setupMenu(self):
        menubar = self.menuBar()

        file_menu: QMenu = menubar.addMenu("&File")
        edit_menu: QMenu = menubar.addMenu("&Edit")
        view_menu: QMenu = menubar.addMenu("&View")

        file_menu.addAction("Save", lambda: print("saved"))
        file_menu.addAction("Open", lambda: print("open"))

        spritePalette_act = self._ui.spritePaletteDock.toggleViewAction()
        spritePalette_act.setShortcut("F3")
        view_menu.addAction(spritePalette_act)

        animEditor_act = self._ui.animEditorDock.toggleViewAction()
        animEditor_act.setShortcut("F4")
        view_menu.addAction(animEditor_act)

        view_menu.addSeparator()
        fullscreen_act = QAction("Full Screen", self)
        fullscreen_act.setShortcut("F11")
        fullscreen_act.triggered.connect(self._fullScreen)
        view_menu.addAction(fullscreen_act)
