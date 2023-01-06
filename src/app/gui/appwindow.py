from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QAction, QMainWindow, QMenu

from ..tool import ToolManager
from .animation import AnimEditorDock
from .editor import EditorScene, EditorView
from .sprite.box import SpriteListBox, SpritePropertyBox
from .sprite.palette import SpritePaletteDock


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._setupUi()
        self._setupMenu()
        self._makeConnections()

    def _setupUi(self):
        self.setWindowTitle("Puppet")
        self.setMinimumSize(800, 600)

        self._ui_graphScene = EditorScene(self, width=2048, height=2048)
        self._ui_graphView = EditorView(self._ui_graphScene, self)
        self._toolManager = ToolManager(self._ui_graphScene)

        self._ui_spritePaletteDock = SpritePaletteDock(self)
        self._ui_animTimelineDock = AnimEditorDock(self)

        self._ui_spritePropertyBox = SpritePropertyBox()
        self._ui_spriteListBox = SpriteListBox()

        self._ui_graphView.addFixedWidget(
            self._ui_spritePropertyBox, Qt.AlignRight | Qt.AlignTop
        )
        self._ui_graphView.addFixedWidget(
            self._ui_spriteListBox, Qt.AlignRight | Qt.AlignBottom
        )

        self.setCentralWidget(self._ui_graphView)
        self.addDockWidget(Qt.BottomDockWidgetArea, self._ui_spritePaletteDock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self._ui_animTimelineDock)

    def _makeConnections(self):
        self._ui_spritePaletteDock.palette.selectedSpriteChanged.connect(
            self._ui_graphScene.addSprite
        )
        self._ui_graphView.selectedItemChanged.connect(
            self._ui_spritePropertyBox.onSelectedItemChanged
        )

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

        animTimeline_act = self._ui_animTimelineDock.toggleViewAction()
        animTimeline_act.setShortcut("F4")
        view_menu.addAction(animTimeline_act)

        view_menu.addSeparator()
        fullscreen_act = QAction("Full Screen", self)
        fullscreen_act.setShortcut("F11")
        fullscreen_act.triggered.connect(self._fullScreen)
        view_menu.addAction(fullscreen_act)
