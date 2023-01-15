from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QAction, QDockWidget, QMainWindow, QMenu

from ..model.chardocument import CharDocument
from .animation import AnimationEditorDock
from .editor import CharEditorWidget
from .palette import SpritePaletteDock


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # document models
        self._document = CharDocument()
        # self._spritesheets = SpriteSheetCollectionModel()

        self._setupUi()
        self._setupMenu()
        # self._makeConnections()

    def _setupUi(self):
        self.setWindowTitle("Puppet Studio")
        self.setMinimumSize(800, 600)

        self._ui_editor = CharEditorWidget(self)
        self.setCentralWidget(self._ui_editor)

        # TODO clean this up
        self._ui_editor.setDocument(self._document)

        self._ui_spritePaletteDock = SpritePaletteDock(self, model=self._document)
        self.addDockWidget(Qt.BottomDockWidgetArea, self._ui_spritePaletteDock)
        self._ui_animEditorDock = AnimationEditorDock(self, model=self._document)
        self.addDockWidget(Qt.BottomDockWidgetArea, self._ui_animEditorDock)

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
