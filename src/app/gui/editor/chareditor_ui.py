from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from ..widget import (
    CustomGraphicScene,
    CustomGraphicSceneOptions,
    CustomGraphicView,
    CustomGraphicViewOptions,
    ZoomSlider,
)
from .spritelistbox import SpriteListBox


class CharEditorUi:
    def setupUi(self, parent: QWidget) -> None:
        self.editorScene = CustomGraphicScene(
            parent, options=CustomGraphicSceneOptions(1024, 1024)
        )

        self.editorView = CustomGraphicView(
            self.editorScene,
            parent,
            options=CustomGraphicViewOptions(True, True, True, 32, True),
        )

        # widgets over the scene viewport
        sliderVbox = QVBoxLayout()
        self.zoomSlider = ZoomSlider(min_=1, max_=25)
        sliderVbox.addStretch()
        sliderVbox.addWidget(self.zoomSlider)

        hbox = QHBoxLayout()
        hbox.addLayout(sliderVbox, 0)
        hbox.addStretch()
        self.spriteListBox = SpriteListBox()
        hbox.addWidget(self.spriteListBox, 0, Qt.AlignRight)

        vbox = QVBoxLayout(self.editorView.viewport())
        vbox.addLayout(hbox)

        main = QHBoxLayout(parent)
        main.addWidget(self.editorView)
