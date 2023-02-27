import typing

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QGraphicsScene, QWidget

from .dope_sheet_editor_ui import DopeSheetEditorUi


class DopeSheetEditor(QWidget):
    def __init__(self, parent: typing.Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self._ui = DopeSheetEditorUi()
        self._ui.setupUi(self)

    def getScene(self) -> QGraphicsScene:
        return self._ui.dopeSheetView.scene()

    def _advance(self) -> None:
        self._ui.dopeSheetView.advance()

    def _rewind(self) -> None:
        self._ui.dopeSheetView.rewind()

    def _setKeyFrame(self) -> None:
        print("not implemented")
