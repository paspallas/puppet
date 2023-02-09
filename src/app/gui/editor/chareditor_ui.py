from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from ..widget import (
    CustomGraphicScene,
    CustomGraphicSceneOptions,
    CustomGraphicView,
    CustomGraphicViewOptions,
    Ruler,
)
from .spritelistbox import SpriteListBox


class CharEditorUi:
    def setupUi(self, parent: QWidget) -> None:
        self.editorScene = CustomGraphicScene(
            parent, options=CustomGraphicSceneOptions(2048, 2048)
        )

        self.editorView = CustomGraphicView(
            self.editorScene,
            parent,
            options=CustomGraphicViewOptions(True, False, True, 32, True),
        )

        self.ruler = Ruler(self.editorView)
        self.ruler.setFixedWidth(int(self.editorScene.width()))
        self.ruler.sizeChanged.connect(
            lambda x: self.editorView.setViewportMargins(0, x.height(), 0, 0)
        )

        # widgets over the scene viewport
        self.spriteListBox = SpriteListBox()
        vbox = QVBoxLayout(self.editorView.viewport())
        vbox.addWidget(self.spriteListBox, 0, Qt.AlignRight)

        hbox = QHBoxLayout(parent)
        hbox.addWidget(self.editorView)
