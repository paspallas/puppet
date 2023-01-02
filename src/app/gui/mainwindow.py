from PyQt5.QtCore import QPoint, QRect, pyqtSlot
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QAction, QMainWindow, QMenu

from app.scene.tool.toolmanager import ToolManager

from .filedialog import DialogFileIO
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
        file_menu.addAction("Open", lambda: self._open())

    @pyqtSlot()
    def _open(self) -> None:
        path_, file_ = DialogFileIO().openFile("Images (*.png)")

        if path_:
            # test add all sprites in the image to the scene
            from spriteutil.spritesheet import SpriteSheet

            from app.model.sprite import Sprite

            texture_sheet = QPixmap(path_)

            sheet = SpriteSheet(path_)
            sprites, _ = sheet.find_sprites()
            for sprite in sprites:
                self._view.scene().addItem(
                    Sprite.fromSpriteSheet(
                        *sprite.top_left, sprite.width, sprite.height, texture_sheet
                    )
                )
