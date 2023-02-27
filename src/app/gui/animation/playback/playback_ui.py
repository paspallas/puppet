from PyQt5.QtWidgets import (
    QAction,
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QToolButton,
    QVBoxLayout,
    QWidget,
)


class PlayBackUi:
    def setupUi(self, parent: QWidget) -> None:
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

        self.currentViewLabel = QLabel("View")
        self.currentView = QComboBox()
        self.currentView.setToolTip("Current edit view")
        self.currentView.addItem("Dope sheet")
        self.currentView.addItem("Easing curve")

        # self.editor = QToolButton()
        # self.editor.setPopupMode(QToolButton.MenuButtonPopup)
        # self.editor.triggered.connect(self.editor.setDefaultAction)
        # self.editor.addAction(QAction("Dopesheet", parent))
        # self.editor.addAction(QAction("Curve editor", parent))

        hbox = QHBoxLayout(parent)
        hbox.setContentsMargins(0, 0, 0, 5)
        hbox.addWidget(self.currentViewLabel)
        hbox.addWidget(self.currentView)
        hbox.addStretch()
        hbox.addWidget(self.followChk)
        hbox.addWidget(self.fpsLabel)
        hbox.addWidget(self.fpsSpin)
        hbox.addWidget(self.lengthSpin)
        hbox.addWidget(self.lengthLabel)
