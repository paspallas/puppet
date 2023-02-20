import typing

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTreeView

from key_frame_item import KeyFrameItem
from timeline import TimeLineView, TimeLineScene
from play_back_controller import PlayBackController
from track_model import TrackModel


class AnimationDock(QWidget):
    def __init__(self, parent: typing.Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self._trackModel = TrackModel()
        self._playBackControl = PlayBackController()

        self._trackView = QTreeView(self)
        self._trackView.setUniformRowHeights(True)
        self._trackView.setModel(self._trackModel)

        self._timeLineScene = TimeLineScene()
        self._timeLineView = TimeLineView(self._timeLineScene, self)

        hbox = QHBoxLayout(self)
        hbox.addWidget(self._trackView, 1)
        hbox.addWidget(self._timeLineView, 5)


if __name__ == "__main__":
    import sys
    from qtmodern import styles
    from PyQt5.QtWidgets import QApplication, QMainWindow

    class Window(QMainWindow):
        def __init__(self) -> None:
            super().__init__()

            self.setWindowTitle("Timeline")
            self.dock = AnimationDock()
            self.setCentralWidget(self.dock)
            self.show()

            self.populate()

        def populate(self) -> None:
            key_1 = KeyFrameItem(10, 60, 10, 20)
            key_2 = KeyFrameItem(160, 60, 150, 20)

            self.dock._timeLineScene.addKeyFrame(key_1)
            self.dock._timeLineScene.addKeyFrame(key_2)

    app = QApplication([])
    styles.dark(app)
    w = Window()
    sys.exit(app.exec_())
