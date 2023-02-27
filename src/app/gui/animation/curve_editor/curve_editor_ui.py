from PyQt5.QtWidgets import QComboBox, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from .curve_editor_view import CurveEditorView


class CurveEditorUi:
    def setupUi(self, parent: QWidget) -> None:
        parent.setMinimumWidth(800)

        self.presetLabel = QLabel("Preset")
        self.presetCombo = QComboBox()
        self.presetCombo.addItems(["Linear", "Cubic", "Sine", "Hold"])
        self.presetLabel.setBuddy(self.presetCombo)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addWidget(self.presetLabel)
        hbox.addWidget(self.presetCombo)
        hbox.addStretch()

        self.view = CurveEditorView()
        self.view.setStyleSheet("background-color: rgb(60, 60, 60)")

        vbox = QVBoxLayout(parent)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addLayout(hbox)
        vbox.addWidget(self.view)
