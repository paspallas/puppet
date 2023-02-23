import typing

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTreeView, QVBoxLayout, QComboBox

from key_frame_item import KeyFrameItem
from timeline import TimeLineView, TimeLineScene
from play_back_controller import PlayBackController
from track_model import TrackModel
from track_item import TrackItem
from track_manager import TrackManager


class AnimationDock(QWidget):
    def __init__(self, parent: typing.Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self._animCombo = QComboBox()
        self._animCombo.addItems(["Iddle", "Run", "Attack"])
        self._trackView = QTreeView()
        self._trackView.setHeaderHidden(True)
        self._trackView.setMouseTracking(True)
        self._trackView.setUniformRowHeights(True)
        self._trackView.setAnimated(True)
        self._trackModel = TrackModel()
        self._trackView.setModel(self._trackModel)

        trackBox = QVBoxLayout()
        trackBox.addSpacing(60)
        trackBox.addWidget(self._animCombo)
        trackBox.addWidget(self._trackView)

        self._timeLineScene = TimeLineScene()
        self._timeLineView = TimeLineView(self._timeLineScene, self)
        self._trackManager = TrackManager(self._timeLineScene)
        self._playBackControl = PlayBackController()

        hbox = QHBoxLayout(self)
        hbox.addLayout(trackBox, 2)
        hbox.addWidget(self._timeLineView, 5)


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
