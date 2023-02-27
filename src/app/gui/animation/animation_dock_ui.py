import typing

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (
    QDockWidget,
    QHBoxLayout,
    QSplitter,
    QWidget,
    QStackedLayout,
    QVBoxLayout,
)

from .curve_editor import CurveEditor
from .dope_sheet import DopeSheetEditor
from .playback import PlayBackControls
from .track_editor import TrackEditor


class AnimationDockUi:
    def setupUi(self, parent: QDockWidget) -> None:
        self.playBackControl = PlayBackControls()
        self.curveEditor = CurveEditor()
        self.dopeSheet = DopeSheetEditor()
        self.trackEditor = TrackEditor()

        self.stack = QStackedLayout()
        self.stack.setContentsMargins(0, 0, 0, 0)
        self.stack.setStackingMode(QStackedLayout.StackOne)
        self.stack.addWidget(self.dopeSheet)
        self.stack.addWidget(self.curveEditor)

        self.playBackControl.sigSelectedViewChanged.connect(self.stack.setCurrentIndex)

        viewBox = QVBoxLayout()
        viewBox.addWidget(self.playBackControl)
        viewBox.addLayout(self.stack)

        self.viewsContainer = QWidget()
        self.viewsContainer.setLayout(viewBox)

        self.splitter = QSplitter(Qt.Horizontal, parent)
        self.splitter.addWidget(self.trackEditor)
        self.splitter.addWidget(self.viewsContainer)

        parent.setWidget(self.splitter)
