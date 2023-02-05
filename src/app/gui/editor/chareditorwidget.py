from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QGraphicsItem, QWidget

from ...model.chardocument import CharDocument
from ...tool import SceneToolManager
from .chareditor_ui import CharEditorUi

from ...tool.rectangle import Rectangle
from ...tool.rectangle_editor import RectangleEditor

from PyQt5.QtCore import QPointF, QRectF


class CharEditorWidget(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._ui = CharEditorUi()
        self._ui.setupUi(self)

        self._toolmanager = SceneToolManager(self._ui.editorScene)
        self._document = None

        self._ui.editorScene.sigSelectedItem.connect(
            self._ui.spriteListBox.setCurrentItem
        )

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
        self._document._currentEditableFrame.sigSelectedItem.connect(
            self._ui.spriteListBox.setCurrentItem
        )

        self._ui.spriteListBox.setModel(self._document._currentFrameModel)
        self._document._currentFrameModel.sigModelDataChanged.connect(
            self._ui.spriteListBox.updateDataMapper
        )

        self.rectangle = Rectangle(QPointF(0, 0), QRectF(0, 0, 100, 100))
        self.rectangleEdit = RectangleEditor(None, self.rectangle)
        self._ui.editorScene.addItem(self.rectangle)
        self._ui.editorScene.addItem(self.rectangleEdit)

    @pyqtSlot(str, bool)
    def sltSetTool(self, tool_cls: str, activate: bool) -> None:
        self._toolmanaget.setTool(tool_cls, activate)
