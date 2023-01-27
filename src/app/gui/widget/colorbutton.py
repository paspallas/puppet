from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QPushButton


class ColorButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setCheckable(False)

        self._default = "#ffffff"
        self.setColor(self._default)

    @pyqtSlot(str)
    def setColor(self, color: str):
        if color:
            self.setStyleSheet(f"background-color: {color}")
        else:
            self.setStyleSheet("")

    def color(self):
        return self._color
