from pathlib import Path

from PyQt5.QtCore import QPoint, QRectF, QSize, QSizeF, Qt, pyqtSlot
from PyQt5.QtGui import QBrush, QColor, QPainter, QPixmap
from PyQt5.QtWidgets import (
    QBoxLayout,
    QDockWidget,
    QFrame,
    QGraphicsItem,
    QGraphicsItemGroup,
    QGraphicsScene,
    QGraphicsView,
    QHBoxLayout,
    QListWidget,
    QMainWindow,
    QToolBar,
    QVBoxLayout,
    QWidget,
)
from spriteutil.spritesheet import SpriteSheet

from app.model.sprite import Sprite, SpriteGroup

from .filedialog import DialogFileIO
from .navcontrol import PanControl, ZoomControl


class SpritePaletteScene(QGraphicsScene):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self._sprite_sheets = dict()

        self.setSceneRect(10, -10, 300, 300)

    def addSpriteSheet(self, name: str, sprites: [Sprite]):
        self.hideAll()

        group = SpriteGroup()
        for sprite in sprites:
            sprite.setPos(sprite.x, sprite.y)
            sprite.lock()
            self.addItem(sprite)
            group.add(sprite)
        group.show()

        self._sprite_sheets[name] = group

    @pyqtSlot()
    def showLayer(self, name: str):
        self.hideAll()
        self._sprite_sheets[name].show()

    def hideAll(self):
        for group in self._sprite_sheets.values():
            group.hide()

    def drawBackground(self, painter: QPainter, rect: QRectF) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(rect, QBrush(QColor("#404040")))


class SpritePaletteView(QGraphicsView):
    def __init__(self, scene: QGraphicsScene, parent: QWidget = None):
        super().__init__(scene, parent)

        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.NoFrame)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setMouseTracking(True)

        ZoomControl(self)
        PanControl(self)


class SpritePalette(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self._scene = SpritePaletteScene()
        self._view = SpritePaletteView(self._scene)

        self._sprite_sheet_list = QListWidget(self)
        self._sprite_sheet_list.itemClicked.connect(
            lambda item: self._scene.showLayer(item.text())
        )

        box = QBoxLayout(QBoxLayout.LeftToRight, self)
        box.setContentsMargins(0, 0, 0, 0)
        self._toolbar = QToolBar()
        self._toolbar.setOrientation(Qt.Vertical)
        self._toolbar.addAction("+", self.addSpriteSheet)

        content = QHBoxLayout()
        content.addWidget(self._sprite_sheet_list)
        content.addWidget(self._view)

        box.addWidget(self._toolbar)
        box.addLayout(content)
        self.setLayout(box)

    @pyqtSlot()
    def addSpriteSheet(self) -> None:
        path, _ = DialogFileIO().openFile("Sprite sheet (*.png)")

        if path:
            name = Path(path).stem
            self._sprite_sheet_list.addItem(name)

            sheet = SpriteSheet(path)
            sprites, _ = sheet.find_sprites()

            sprite_sheet = QPixmap(path)
            layer = [
                Sprite.fromSpriteSheet(
                    *sprite.top_left, sprite.width, sprite.height, sprite_sheet
                )
                for sprite in sprites
            ]

            self._scene.addSpriteSheet(name, layer)


class SpritePaletteDock(QDockWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__("Sprite Palette", parent)

        self.setWidget(SpritePalette(self))
