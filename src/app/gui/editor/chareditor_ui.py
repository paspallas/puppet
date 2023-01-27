from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from ..widget import (
    CustomGraphicScene,
    CustomGraphicSceneOptions,
    CustomGraphicView,
    CustomGraphicViewOptions,
)
from .spritelistbox import SpriteListBox


class CharEditorUi:
    def setupUi(self, parent: QWidget) -> None:
        self.editorScene = CustomGraphicScene(
            parent, options=CustomGraphicSceneOptions(2048, 2048, 32, True)
        )

        self.editorView = CustomGraphicView(
            self.editorScene,
            parent,
            options=CustomGraphicViewOptions(True, False, True),
        )

        # widgets over the scene viewport
        self.spriteListBox = SpriteListBox()
        vbox = QVBoxLayout(self.editorView.viewport())
        vbox.addWidget(self.spriteListBox, 0, Qt.AlignRight)

        hbox = QHBoxLayout(parent)
        hbox.addWidget(self.editorView)
