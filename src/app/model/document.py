from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot


class Document(QObject):
    """Keeps track of a file an its undo history"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
