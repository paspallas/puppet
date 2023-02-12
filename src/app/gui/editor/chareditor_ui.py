from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from ..widget import (
    CustomGraphicScene,
    CustomGraphicSceneOptions,
    CustomGraphicView,
    CustomGraphicViewOptions,
    ZoomSlider,
)
from ..viewcontrol import ZoomControl, PanControl
from .spritelistbox import SpriteListBox


class CharEditorUi:
    __max_zoom__ = 25
    __min_zoom__ = 1

    def setupUi(self, parent: QWidget) -> None:
        self.editorScene = CustomGraphicScene(
            parent, options=CustomGraphicSceneOptions(1024, 1024)
        )

        self.editorView = CustomGraphicView(
            self.editorScene,
            parent,
            options=CustomGraphicViewOptions(True, True, True, 32, True),
        )

        PanControl(self.editorView)
        zoom = ZoomControl(self.editorView, self.__min_zoom__, self.__max_zoom__)

        # set widgets over the scene viewport
        self.zoomSlider = ZoomSlider(min_=self.__min_zoom__, max_=self.__max_zoom__)
        self.zoomSlider.zoomChanged.connect(zoom.setValue)
        zoom.zoomLevelChanged.connect(self.zoomSlider.setValue)

        sliderVbox = QVBoxLayout()
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
