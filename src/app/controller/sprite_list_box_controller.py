from PyQt5.QtCore import QObject, Qt, pyqtSignal, pyqtSlot


class SpriteListBoxController(QObject):
    def __init__(self) -> None:
        super().__init__()