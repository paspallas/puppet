from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QAction, QDockWidget, QMainWindow, QMenu

from ..model.chardocument import CharDocument
from .animation import AnimationEditorDock
from .editor import CharEditorWidget
from .palette import SpritePaletteDock

from ..model.animation_frame import AnimationFrame
from ..model.animation_frame_model import AnimationFrameModel
from ..model.animation_frame_sprite import FrameSprite


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Puppet Studio")
        self.setMinimumSize(800, 600)

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

        self._animFrameModel = AnimationFrameModel()
        self._animFrameModel.setDataSource(self._animFrame)

        # self._makeConnections()

        self._ui_editor = CharEditorWidget(self)
        self.setCentralWidget(self._ui_editor)

        #! test passing the model to the main editor
        self._ui_editor.setModel(self._animFrameModel)

        # TODO clean this up
        self._ui_editor.setDocument(self._document)

        self._ui_spritePaletteDock = SpritePaletteDock(self, model=self._document)
        self._ui_animEditorDock = AnimationEditorDock(self, model=self._document)
        self.addDockWidget(Qt.BottomDockWidgetArea, self._ui_spritePaletteDock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self._ui_animEditorDock)

        self._setupMenu()

    # def _makeConnections(self):
    #     self._ui_spritePaletteWid.sigSelectedSprite.connect(
    #         self._ui_editor.sltAddSprite
    #     )

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

        spritePalette_act = self._ui_spritePaletteDock.toggleViewAction()
        spritePalette_act.setShortcut("F3")
        view_menu.addAction(spritePalette_act)

        animEditor_act = self._ui_animEditorDock.toggleViewAction()
        animEditor_act.setShortcut("F4")
        view_menu.addAction(animEditor_act)

        view_menu.addSeparator()
        fullscreen_act = QAction("Full Screen", self)
        fullscreen_act.setShortcut("F11")
        fullscreen_act.triggered.connect(self._fullScreen)
        view_menu.addAction(fullscreen_act)
