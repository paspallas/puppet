import typing

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget

from ..widget import MaximizableDock
from .animation_dock_ui import AnimationDockUi
from .track_manager import TrackManager


class AnimationEditorDock(MaximizableDock):
    def __init__(self, parent: typing.Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Animation")
        self.setAllowedAreas(Qt.BottomDockWidgetArea)

        self._ui = AnimationDockUi()
        self._ui.setupUi(self)
        self.TestPopulate()

    @pyqtSlot()
    def advance(self) -> None:
        self._ui.dopeSheet._advance()

    @pyqtSlot()
    def rewind(self) -> None:
        self._ui.dopeSheet._rewind()

    @pyqtSlot()
    def setKeyframe(self) -> None:
        self._ui.dopeSheet._setKeyFrame()

    def TestPopulate(self) -> None:
        self._trackManager = TrackManager(self._ui.dopeSheet.getScene())
        self._trackManager.newTrack()
        self._trackManager.addPropertyTrack(0)
        self._trackManager.addPropertyTrack(0)
        self._trackManager.addPropertyTrack(0)
        self._trackManager.addPropertyTrack(0)
        self._trackManager.newTrack()
        self._trackManager.addPropertyTrack(1)
        self._trackManager.addPropertyTrack(1)
        self._trackManager.addPropertyTrack(1)
        self._trackManager.newTrack()
        self._trackManager.addPropertyTrack(2)
        self._trackManager.addPropertyTrack(2)
        self._trackManager.newTrack()
        self._trackManager.addPropertyTrack(3)
        self._trackManager.addPropertyTrack(3)
        self._trackManager.newTrack()
        self._trackManager.addPropertyTrack(4)
        self._trackManager.addPropertyTrack(4)
        self._trackManager.newTrack()
        self._trackManager.addPropertyTrack(5)
        self._trackManager.addPropertyTrack(5)
        self._trackManager.newTrack()
        self._trackManager.addPropertyTrack(6)
        self._trackManager.addPropertyTrack(6)
        self._trackManager.newTrack()
        self._trackManager.addPropertyTrack(7)
        self._trackManager.addPropertyTrack(7)
