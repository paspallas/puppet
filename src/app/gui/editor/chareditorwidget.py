from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QGraphicsItem, QWidget

from ...model.chardocument import CharDocument
from ...tool import SceneToolManager
from .chareditor_ui import CharEditorUi


class CharEditorWidget(QWidget):

    sigSelectedItemChanged = pyqtSignal(QGraphicsItem)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._ui = CharEditorUi()
        self._ui.setupUi(self)

        self._toolmanager = SceneToolManager(self._ui.editorScene)
        self._document: CharDocument = None

    def setDocument(self, document: CharDocument) -> None:
        if self._document is not None:
            self._document._currentEditableFrame.sigAddToScene.disconnect()
            self._document._currentEditableFrame.sigDeleteFromScene.disconnect()

        self._document = document
        self._document._currentEditableFrame.sigAddToScene.connect(
            lambda item: self._ui.editorScene.addItem(item)
        )
        self._document._currentEditableFrame.sigDeleteFromScene.connect(
            lambda item: self._ui.editorScene.removeItem(item)
        )

        self._ui.spriteListBox.setModel(self._document._currentFrameModel)

    @pyqtSlot(QGraphicsItem)
    def sltAddSprite(self, sprite: QGraphicsItem) -> None:
        sprite.unlock()
        self._ui.editorScene.addItem(sprite)

    @pyqtSlot(str, bool)
    def sltSetTool(self, tool_cls: str, activate: bool) -> None:
        self._toolmanaget.setTool(tool_cls, activate)
