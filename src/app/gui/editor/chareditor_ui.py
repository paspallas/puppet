from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QWidget

from .chareditorscene import CharEditorScene
from .chareditorview import CharEditorView
from .spritelistbox import SpriteListBox
from .spritepropertybox import SpritePropertyBox


class CharEditorUi:
    def setupUi(self, parent: QWidget) -> None:
        self.editorScene = CharEditorScene(parent)
        self.editorView = CharEditorView(self.editorScene, parent)
        self.spritePropertyBox = SpritePropertyBox()
        self.spriteListBox = SpriteListBox()

        self.editorView.addFixedWidget(
            self.spritePropertyBox, Qt.AlignRight | Qt.AlignTop
        )
        self.editorView.addFixedWidget(
            self.spriteListBox, Qt.AlignRight | Qt.AlignBottom
        )

        hbox = QHBoxLayout(parent)
        hbox.addWidget(self.editorView)
