from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QGraphicsItem, QWidget

from ...model.document import Document
from ...tool import SceneToolManager
from .char_editor_ui import CharEditorUi


class CharEditorWidget(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._ui = CharEditorUi()
        self._ui.setupUi(self)

        self._toolmanager = SceneToolManager(self._ui.editorScene)
        self._document: Document = None

        self.makeConnections()

    def makeConnections(self) -> None:
        # self._ui.editorScene.sigSelectedItem.connect(
        #     self._ui.spriteListBox.setCurrentItem
        # )
        self._ui.editorScene.sigNoItemSelected.connect(
            self._ui.spriteListBox.clearSelection
        )
        self._ui.spriteListBox.sigEnabledChanged.connect(
            self._ui.spriteProperty.setEnabled
        )
        self._ui.spriteListBox.sigItemChanged.connect(
            self._ui.spriteProperty.onSelectedItemChanged
        )

    def setDocument(self, document: Document) -> None:
        if self._document is not None:
            self._document._currentEditableFrame.sigAddToScene.disconnect()
            self._document._currentEditableFrame.sigDeleteFromScene.disconnect()

        self._document = document
        self._document._currentEditableFrame.sigAddToScene.connect(
            self._ui.editorScene.addItem
        )
        self._document._currentEditableFrame.sigDeleteFromScene.connect(
            self._ui.editorScene.removeItem
        )
        self._document._currentEditableFrame.sigSelectedItem.connect(
            self._ui.spriteListBox.setCurrentItem
        )

        self._ui.spriteProperty.setModel(self._document._currentFrameModel)
        self._ui.spriteListBox.setModel(self._document._currentFrameModel)

    @pyqtSlot(str, bool)
    def setTool(self, tool_cls: str, activate: bool) -> None:
        self._toolmanaget.setTool(tool_cls, activate)

    @pyqtSlot(bool)
    def toggleSpritePropertyVisibility(self, visible: bool) -> None:
        self._ui.spriteListBox.setVisible(not visible)
        self._ui.spriteProperty.setVisible(not visible)
