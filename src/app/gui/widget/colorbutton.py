from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QMouseEvent
from PyQt5.QtWidgets import QColorDialog, QPushButton

from .colorpicker import ColorPickerWidget


class ColorButton(QPushButton):
    colorChanged = pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._color = None
        self._default = "#ffffff"
        self.pressed.connect(self.onColorPicker)

        self.setColor(self._default)

    def setColor(self, color):
        if color != self._color:
            self._color = color
            self.colorChanged.emit(color)

        if self._color:
            self.setStyleSheet(f"background-color: {self._color}")
        else:
            self.setStyleSheet("")

    def color(self):
        return self._color

    def onColorPicker(self):
        """Show the color picker"""

        self._ui_colorPickerWid = ColorPickerWidget()
        self._ui_colorPickerWid.show()
        # dialog = QColorDialog(self)
        # if self._color:
        #     dialog.setCurrentColor(QColor(self._color))

        # if dialog.exec_():
        #     self.setColor(dialog.currentColor().name())
        #     print(dialog.currentColor().name())

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.RightButton:
            self.setColor(self._default)

        super().mousePressEvent(e)
