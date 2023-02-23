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
        self._animCombo.addItems(["Iddle", "Run", "Attack"])
        self._newAnimBtn = QPushButton("+", self)
        self._delAnimBtn = QPushButton("-", self)

        animBox = QHBoxLayout()
        animBox.addWidget(self._animCombo)
        animBox.addStretch()
        animBox.addWidget(self._newAnimBtn, 0, Qt.AlignLeft)
        animBox.addWidget(self._delAnimBtn, 0, Qt.AlignLeft)

        trackBox = QVBoxLayout()
        trackBox.addLayout(animBox)
        trackBox.addWidget(self._trackView)

        self._timeLineScene = TimeLineScene()
        self._timeLineView = TimeLineView(self._timeLineScene, self)
        self._trackManager = TrackManager(self._timeLineScene)
        self._playBackControl = PlayBackController()

        self._fpsLabel = QLabel("Fps", self)
        self._fpsSpin = QSpinBox(self)
        self._fpsSpin.setRange(1, 60)
        self._fpsSpin.setValue(15)

        self._lengthLabel = QLabel("Length", self)
        self._lengthSpin = QSpinBox(self)
        self._lengthSpin.setRange(60, 2000)

        playbackBox = QHBoxLayout()
        playbackBox.addStretch()
        playbackBox.addWidget(self._fpsLabel)
        playbackBox.addWidget(self._fpsSpin)
        playbackBox.addSpacing(30)
        playbackBox.addWidget(self._lengthLabel)
        playbackBox.addWidget(self._lengthSpin)

        timelineBox = QVBoxLayout()
        timelineBox.addLayout(playbackBox)
        timelineBox.addWidget(self._timeLineView)

        hbox = QHBoxLayout(self)
        hbox.addLayout(trackBox, 2)
        hbox.addLayout(timelineBox, 5)


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
