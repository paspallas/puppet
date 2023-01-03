from PyQt5.QtCore import QPoint, QRect, Qt, pyqtSlot
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QAction, QMainWindow, QMenu, QGraphicsView, QGraphicsScene

from app.scene.tool.toolmanager import ToolManager

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

        # self._view.addFixedWidget(PropertyBox(), Qt.AlignRight | Qt.AlignTop)
        # self._view.addFixedWidget(self._sprite_palette, Qt.AlignLeft | Qt.AlignBottom)

        self.setupUi()
        self.setupMenu()

    def setupUi(self):
        self.setWindowTitle("MegaPuppet")
        self.setMinimumSize(800, 600)
        self.setCentralWidget(self._view)
        self.addDockWidget(Qt.BottomDockWidgetArea, self._sprite_palette)

    def setupMenu(self):
        menubar = self.menuBar()

        file_menu: QMenu = menubar.addMenu("File")
        edit_menu: QMenu = menubar.addMenu("Edit")

        settings_menu: QMenu = menubar.addMenu("Settings")

        file_menu.addAction("Save", lambda: print("saved"))
        file_menu.addAction("Open", lambda: print("open"))
