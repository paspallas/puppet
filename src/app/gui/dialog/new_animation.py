import typing

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLineEdit, QVBoxLayout, QWidget


class NewAnimationDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Create new animation")
        self.setFixedSize(300, 100)

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self._buttonBox = QDialogButtonBox(buttons)
        self._buttonBox.accepted.connect(self.accept)
        self._buttonBox.rejected.connect(self.reject)

        self._name = QLineEdit("Name")

        self._vbox = QVBoxLayout(self)
        self._vbox.addWidget(self._name)
        self._vbox.addStretch()
        self._vbox.addWidget(self._buttonBox)

    def name(self) -> str:
        name = self._name.text().lstrip().rstrip()

        if len(name) > 0:
            return name.replace(" ", "_")

        return "New_animation"
