import typing

from PyQt5.QtCore import QObject, Qt, QTimer, pyqtSignal, pyqtSlot


class PlayBackController(QObject):
    def __init__(self) -> None:
        super().__init__()

        self._timer = QTimer()
        self._timer.timeout.connect(self.updatePlayBack)

    def play(self) -> None:
        self._timer.startTimer(16, Qt.PreciseTimer)
        self._timer.start()

    def stop(self) -> None:
        self._timer.stop()

    def rewind(self) -> None:
        pass

    def updatePlayBack(self) -> None:
        NotImplemented
