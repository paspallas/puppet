import typing

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QTreeView,
    QVBoxLayout,
    QComboBox,
    QSpinBox,
    QLabel,
    QPushButton,
    QSplitter,
    QCheckBox,
)

from key_frame_item import KeyFrameItem
from timeline import TimeLineView, TimeLineScene
from play_back_controller import PlayBackController
from track_model import TrackModel
from track_item import TrackItem
from track_manager import TrackManager


class AnimationDock(QWidget):
    def __init__(self, parent: typing.Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self._trackView = QTreeView()
        self._trackView.setHeaderHidden(True)
        self._trackView.setMouseTracking(True)
        self._trackView.setUniformRowHeights(True)
        self._trackView.setAlternatingRowColors(True)
        self._trackModel = TrackModel()
        self._trackView.setModel(self._trackModel)

        self._animCombo = QComboBox()
        self._animCombo.setFixedWidth(150)
        self._animCombo.addItems(["Iddle", "Run", "Attack"])
        self._newAnimBtn = QPushButton("+")
        self._delAnimBtn = QPushButton("-")

        animBox = QHBoxLayout()
        animBox.addWidget(self._animCombo)
        animBox.addStretch()
        animBox.addWidget(self._newAnimBtn)
        animBox.addWidget(self._delAnimBtn)

        trackBox = QVBoxLayout()
        trackBox.addLayout(animBox)
        trackBox.addWidget(self._trackView)

        self._timeLineScene = TimeLineScene()
        self._timeLineView = TimeLineView(self._timeLineScene)
        self._trackManager = TrackManager(self._timeLineScene)
        self._playBackControl = PlayBackController()

        self._followChk = QCheckBox("Follow")
        self._followChk.setToolTip("Follow playhead")
        self._followChk.stateChanged.connect(self._timeLineView.setFollowPlayHead)

        self._fpsLabel = QLabel("Fps")
        self._fpsSpin = QSpinBox()
        self._fpsSpin.setToolTip("Playback speed")
        self._fpsSpin.setRange(1, 60)
        self._fpsSpin.setValue(15)

        self._lengthLabel = QLabel("Length")
        self._lengthSpin = QSpinBox()
        self._lengthSpin.setRange(60, 2000)
        self._lengthSpin.setToolTip("Max animation length")

        playbackBox = QHBoxLayout()
        playbackBox.addStretch()
        playbackBox.addWidget(self._followChk)
        playbackBox.addWidget(self._fpsLabel)
        playbackBox.addWidget(self._fpsSpin)
        playbackBox.addWidget(self._lengthLabel)
        playbackBox.addWidget(self._lengthSpin)

        timelineBox = QVBoxLayout()
        timelineBox.addLayout(playbackBox)
        timelineBox.addWidget(self._timeLineView)

        self._rightWidget = QWidget()
        self._rightWidget.setLayout(timelineBox)
        self._leftWidget = QWidget()
        self._leftWidget.setLayout(trackBox)

        self._splitter = QSplitter(Qt.Horizontal)
        self._splitter.addWidget(self._leftWidget)
        self._splitter.addWidget(self._rightWidget)
        self._splitter.setStretchFactor(0, 1)
        self._splitter.setStretchFactor(1, 5)

        hbox = QHBoxLayout(self)
        hbox.addWidget(self._splitter)


if __name__ == "__main__":
    import sys
    from qtmodern import styles
    from PyQt5.QtWidgets import QApplication, QMainWindow

    class Window(QMainWindow):
        def __init__(self) -> None:
            super().__init__()

            self.setWindowTitle("Dope Sheet")
            self.dock = AnimationDock()
            self.setCentralWidget(self.dock)
            self.show()

            self.populate()

        def populate(self) -> None:
            key_1 = KeyFrameItem(50, 60, 10, 20)
            key_2 = KeyFrameItem(160 + 50, 60, 150, 20)

            self.dock._trackManager.newTrack()
            self.dock._trackManager.addPropertyTrack(0)
            self.dock._trackManager.addPropertyTrack(0)
            self.dock._trackManager.addPropertyTrack(0)
            self.dock._trackManager.addPropertyTrack(0)

            self.dock._trackManager.newTrack()
            self.dock._trackManager.addPropertyTrack(1)
            self.dock._trackManager.addPropertyTrack(1)
            self.dock._trackManager.addPropertyTrack(1)

            self.dock._trackManager.newTrack()
            self.dock._trackManager.addPropertyTrack(2)
            self.dock._trackManager.addPropertyTrack(2)

            self.dock._trackManager.newTrack()

            # self.dock._trackManager.newTrack()
            # self.dock._trackManager.newTrack()
            # self.dock._trackManager.newTrack()
            # self.dock._trackManager.newTrack()

            # self.dock._timeLineScene.addItem(key_1)
            # self.dock._timeLineScene.addItem(key_2)

    app = QApplication([])
    styles.dark(app)
    w = Window()
    sys.exit(app.exec_())
