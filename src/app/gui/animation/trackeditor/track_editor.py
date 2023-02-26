import typing

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget

from .track_editor_ui import TrackEditorUi


class TrackEditor(QWidget):
    def __init__(self, parent: typing.Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self._ui = TrackEditorUi()
        self._ui.setupUi(self)
