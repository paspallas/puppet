import typing

from PyQt5.QtCore import Qt, pyqtSlot, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)


class NewAnimationDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Create a new animation")
        self.setFixedSize(300, 100)

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self._buttonBox = QDialogButtonBox(buttons)
        self._buttonBox.accepted.connect(self.accept)
        self._buttonBox.rejected.connect(self.reject)

        self._name = QLineEdit("")
        self._name.setValidator(QRegExpValidator(QRegExp("[a-zA-Z0-9_()]*")))
        self._label = QLabel("Name")

        hbox = QHBoxLayout()
        hbox.addWidget(self._label)
        hbox.addWidget(self._name)

        vbox = QVBoxLayout(self)
        vbox.addLayout(hbox)
        vbox.addStretch()
        vbox.addWidget(self._buttonBox)

    def name(self) -> str:
        return self._name.text()
