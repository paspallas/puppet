from PyQt5.QtWidgets import QAction, QMainWindow, QMenu

from app.scene.tool.toolmanager import ToolManager

from .graphicscene import GraphicScene
from .graphicview import GraphicView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._scene = GraphicScene(self, width=2048, height=2048)
        self._view = GraphicView(self, self._scene)
        self._toolmanager = ToolManager(self._scene)

        self.setupUi()
        self.setupMenu()

    def setupUi(self):
        self.setWindowTitle("MegaPuppet")
        self.setMinimumSize(800, 600)
        self.setCentralWidget(self._view)

    def setupMenu(self):
        menubar = self.menuBar()

        file_menu: QMenu = menubar.addMenu("File")
        edit_menu: QMenu = menubar.addMenu("Edit")
        settings_menu: QMenu = menubar.addMenu("Settings")

        file_menu.addAction("Save", lambda: print("saved"))
