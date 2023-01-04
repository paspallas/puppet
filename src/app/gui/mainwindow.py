from PyQt5.QtCore import QPoint, QRect, Qt, pyqtSlot
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QAction, QMainWindow, QMenu, QGraphicsView, QGraphicsScene

from app.scene.tool.toolmanager import ToolManager

from .animation.animedit import AnimEditorDock
from .filedialog import DialogFileIO
from .graphicscene import GraphicScene
from .graphicview import GraphicView
from .scenetoolbox import PropertyBox
from .spritepalette import SpritePaletteDock


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._scene = GraphicScene(self, width=2048, height=2048)
        self._view = GraphicView(self, self._scene)
        self._toolmanager = ToolManager(self._scene)
        self._sprite_palette = SpritePaletteDock(self)
        self._animation_timeline = AnimEditorDock(self)
        self._sprite_property = PropertyBox()

        self._view.addFixedWidget(self._sprite_property, Qt.AlignRight | Qt.AlignTop)

        self.setupUi()
        self.setupMenu()
        self.makeConnections()

    def setupUi(self):
        self.setWindowTitle("MegaPuppet")
        self.setMinimumSize(800, 600)
        self.setCentralWidget(self._view)
        self.addDockWidget(Qt.BottomDockWidgetArea, self._sprite_palette)
        self.addDockWidget(Qt.BottomDockWidgetArea, self._animation_timeline)

    def makeConnections(self):
        self._sprite_palette.palette.selectedSpriteChanged.connect(
            self._scene.addSprite
        )
        self._view.selectedItemChanged.connect(
            self._sprite_property.onSelectedItemChanged
        )

    def _fullScreen(self):
        if self.windowState() & Qt.WindowMaximized:
            self.setWindowState(Qt.WindowFullScreen)
        else:
            self.setWindowState(Qt.WindowMaximized)

    def setupMenu(self):
        menubar = self.menuBar()

        file_menu: QMenu = menubar.addMenu("&File")
        edit_menu: QMenu = menubar.addMenu("&Edit")
        view_menu: QMenu = menubar.addMenu("&View")

        file_menu.addAction("Save", lambda: print("saved"))
        file_menu.addAction("Open", lambda: print("open"))

        sprite_palette = self._sprite_palette.toggleViewAction()
        sprite_palette.setShortcut("F3")
        view_menu.addAction(sprite_palette)

        animation_timeline = self._animation_timeline.toggleViewAction()
        animation_timeline.setShortcut("F4")
        view_menu.addAction(animation_timeline)

        view_menu.addSeparator()
        fullscreen = QAction("Full Screen", self)
        fullscreen.setShortcut("F11")
        fullscreen.triggered.connect(self._fullScreen)
        view_menu.addAction(fullscreen)
