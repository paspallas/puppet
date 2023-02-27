import typing

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget

from .playback_ui import PlayBackUi


class PlayBackControls(QWidget):
    sigSelectedViewChanged = pyqtSignal(int)

    def __init__(self, parent: typing.Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self._ui = PlayBackUi()
        self._ui.setupUi(self)

        self._makeConnections()

    def _makeConnections(self) -> None:
        self._ui.currentView.activated.connect(self.sigSelectedViewChanged)
