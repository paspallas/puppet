import typing

from PyQt5.QtCore import QObject, Qt, pyqtSignal, pyqtSlot

from ...dialog import NewAnimationDialog


class TrackEditorController(QObject):
    sigCreateNewAnimation = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()

    @pyqtSlot()
    def newAnimation(self) -> None:
        dialog = NewAnimationDialog()
        if dialog.exec_() == NewAnimationDialog.Accepted:
            name = dialog.name()
            self.sigCreateNewAnimation.emit(name)
