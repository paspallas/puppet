from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QAction, QMainWindow, QMenu, QDockWidget

from .animation import AnimationEditorWidget
from .editor import CharEditorWidget
from .palette import SpritePaletteWidget


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._setupUi()
        self._createDockWindows()
        self._setupMenu()
        self._makeConnections()

    def _setupUi(self):
        self.setWindowTitle("Puppet Studio")
        self.setMinimumSize(800, 600)

        self._ui_editor = CharEditorWidget(self)
        self.setCentralWidget(self._ui_editor)

    def _makeConnections(self):
        self._ui_spritePaletteWid.sigSelectedSpriteChanged.connect(
            self._ui_editor.sltAddSprite
        )

    def _createDockWindows(self):
        self._ui_spritePaletteDock = QDockWidget("Sprite Palette", self)
        self._ui_spritePaletteDock.setAllowedAreas(Qt.BottomDockWidgetArea)
        self._ui_spritePaletteWid = SpritePaletteWidget(self._ui_spritePaletteDock)
        self._ui_spritePaletteDock.setWidget(self._ui_spritePaletteWid)
        self.addDockWidget(Qt.BottomDockWidgetArea, self._ui_spritePaletteDock)

        self._ui_animEditorDock = QDockWidget("Animation Editor", self)
        self._ui_animEditorDock.setAllowedAreas(Qt.BottomDockWidgetArea)
        self._ui_animEditorWidget = AnimationEditorWidget(self._ui_animEditorDock)
        self._ui_animEditorDock.setWidget(self._ui_animEditorWidget)
        self.addDockWidget(Qt.BottomDockWidgetArea, self._ui_animEditorDock)

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
