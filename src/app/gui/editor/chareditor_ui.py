from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from .chareditorscene import CharEditorScene
from .chareditorview import CharEditorView
from .spritelistbox import SpriteListBox


class CharEditorUi:
    def setupUi(self, parent: QWidget) -> None:
        self.editorScene = CharEditorScene(parent)
        self.editorView = CharEditorView(self.editorScene, parent)

        # widgets over the scene viewport
        self.spriteListBox = SpriteListBox()
        vbox = QVBoxLayout(self.editorView.viewport())
        vbox.addStretch(1)
        vbox.addWidget(self.spriteListBox, 0, Qt.AlignRight)
        vbox.addStretch(1)

        hbox = QHBoxLayout(parent)
        hbox.addWidget(self.editorView)
