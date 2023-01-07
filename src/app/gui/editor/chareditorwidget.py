from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QHBoxLayout, QGraphicsScene, QGraphicsView, QWidget

from app.model.sprite import Sprite

from .chareditorscene import CharEditorScene
from .chareditorview import CharEditorView
from .spritelistbox import SpriteListBox
from .spritepropertybox import SpritePropertyBox
from ...tool import SceneToolManager


class CharEditorWidget(QWidget):

    sigSelectedItemChanged = pyqtSignal(Sprite)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._setupUi()
        self._makeConnections()

        self._toolmanager = SceneToolManager(self._ui_editorScene)

    def _setupUi(self) -> None:
        self._ui_editorScene = CharEditorScene(self, width=2048, height=2048)
        self._ui_editorView = CharEditorView(self._ui_editorScene, self)
        self._ui_spritePropertyBox = SpritePropertyBox()
        self._ui_spriteListBox = SpriteListBox()

        self._ui_editorView.addFixedWidget(
            self._ui_spritePropertyBox, Qt.AlignRight | Qt.AlignTop
        )
        self._ui_editorView.addFixedWidget(
            self._ui_spriteListBox, Qt.AlignRight | Qt.AlignBottom
        )

        hbox = QHBoxLayout(self)
        hbox.addWidget(self._ui_editorView)

    def _makeConnections(self) -> None:
        self._ui_editorView.sigSelectedItemChanged.connect(
            self._ui_spritePropertyBox.sltOnSelectedItemChanged
        )

    @pyqtSlot(Sprite)
    def sltAddSprite(self, sprite: Sprite):
        self._ui_editorScene.addItem(sprite)

    @pyqtSlot(str, bool)
    def sltSetTool(self, tool_cls: str, activate: bool) -> None:
        self._toolmanaget.setTool(tool_cls, activate)
