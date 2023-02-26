import typing

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QSpinBox,
    QLabel,
    QPushButton,
    QCheckBox,
)

from .dope_sheet_view import DopeSheetView


class DopeSheetEditorUi:
    def setupUi(self, parent: QWidget) -> None:
        parent.setMinimumWidth(800)

        self.dopeSheetView = DopeSheetView()

        self.followChk = QCheckBox("Follow")
        self.followChk.setToolTip("Follow playhead")
        self.followChk.setChecked(True)

        self.fpsLabel = QLabel("Fps")
        self.fpsSpin = QSpinBox()
        self.fpsSpin.setToolTip("Playback speed")
        self.fpsSpin.setRange(1, 60)
        self.fpsSpin.setValue(15)

        self.lengthLabel = QLabel("Length")
        self.lengthSpin = QSpinBox()
        self.lengthSpin.setRange(60, 2000)
        self.lengthSpin.setToolTip("Max animation length in frames")

        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.followChk)
        hbox.addWidget(self.fpsLabel)
        hbox.addWidget(self.fpsSpin)
        hbox.addWidget(self.lengthSpin)
        hbox.addWidget(self.lengthLabel)

        vbox = QVBoxLayout(parent)
        vbox.addLayout(hbox)
        vbox.addWidget(self.dopeSheetView)
