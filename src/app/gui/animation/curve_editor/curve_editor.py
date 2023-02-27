import typing

from PyQt5.QtWidgets import QWidget

from .curve_editor_ui import CurveEditorUi


class CurveEditor(QWidget):
    def __init__(self, parent: typing.Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self._ui = CurveEditorUi()
        self._ui.setupUi(self)
