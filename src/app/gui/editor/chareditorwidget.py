from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QGraphicsItem, QWidget

from ...model.chardocument import CharDocument
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

        self._currentDoc: CharDocument = None

    def _makeConnections(self) -> None:
        pass
        # self._ui.editorView.sigSelectedItemChanged.connect(
        #     self._ui.spritePropertyBox.sltOnSelectedItemChanged
        # )

    def setDocument(self, document: CharDocument) -> None:
        self._currentDoc = document

        # subscribe to document events
        self._currentDoc.sigSpriteAddedToCollection.connect(self.sltAddSprite)

    def setModel(self, model) -> None:
        self._ui.spriteListBox.setModel(model)

    @pyqtSlot(QGraphicsItem)
    def sltAddSprite(self, sprite: QGraphicsItem):
        sprite.unlock()
        self._ui.editorScene.addItem(sprite)

    @pyqtSlot(str, bool)
    def sltSetTool(self, tool_cls: str, activate: bool) -> None:
        self._toolmanaget.setTool(tool_cls, activate)
