import typing

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QDockWidget, QHBoxLayout, QSplitter

from .dopesheet import DopeSheetEditor
from .trackeditor import TrackEditor


class AnimationDockUi:
    def setupUi(self, parent: QDockWidget) -> None:
        self.dopeSheet = DopeSheetEditor()
        self.trackEditor = TrackEditor()

        self.splitter = QSplitter(Qt.Horizontal, parent)
        self.splitter.addWidget(self.trackEditor)
        self.splitter.addWidget(self.dopeSheet)

        parent.setWidget(self.splitter)
