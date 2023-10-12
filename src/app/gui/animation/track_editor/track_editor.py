import typing

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget

from .track_editor_controller import TrackEditorController
from .track_editor_ui import TrackEditorUi
from .track_model_adapter import TrackModelAdapter


class TrackEditor(QWidget):
    def __init__(self, parent: typing.Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self._controller = TrackEditorController()
        self._ui = TrackEditorUi()
        self._ui.setupUi(self)

        self._ui.newAnimBtn.clicked.connect(self._controller.newAnimation)

        self._controller.sigCreateNewAnimation.connect(self._ui.animCombo.addItem)

        self.setDocument(None)

    def setDocument(self, document) -> None:
        self._document = document
        self._ui.trackTree.setModel(TrackModelAdapter())
