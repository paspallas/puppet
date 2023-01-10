from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QGraphicsItem, QWidget

from ...tool import SceneToolManager
from .chareditor_ui import CharEditorUi


class CharEditorWidget(QWidget):

    sigSelectedItemChanged = pyqtSignal(QGraphicsItem)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._ui = CharEditorUi()
        self._ui.setupUi(self)

        self._makeConnections()
        self._toolmanager = SceneToolManager(self._ui.editorScene)

    def _makeConnections(self) -> None:
        self._ui.editorView.sigSelectedItemChanged.connect(
            self._ui.spritePropertyBox.sltOnSelectedItemChanged
        )

    @pyqtSlot(QGraphicsItem)
    def sltAddSprite(self, sprite: QGraphicsItem):
        self._ui.editorScene.addItem(sprite)

    @pyqtSlot(str, bool)
    def sltSetTool(self, tool_cls: str, activate: bool) -> None:
        self._toolmanaget.setTool(tool_cls, activate)
