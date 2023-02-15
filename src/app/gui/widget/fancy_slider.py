import typing

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSlider, QWidget


class FancySlider(QWidget):
    actionTriggered = pyqtSignal(int)
    rangeChanged = pyqtSignal(int, int)
    sliderMoved = pyqtSignal(int)
    sliderPressed = pyqtSignal()
    sliderReleased = pyqtSignal()
    valueChanged = pyqtSignal(int)

    def __init__(self, parent: typing.Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self._slider = QSlider(Qt.Horizontal)
        self._label = QLabel("", self)
        self._label.setMinimumWidth(20)
        self._label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self._slider.actionTriggered.connect(self.actionTriggered)
        self._slider.rangeChanged.connect(self.rangeChanged)
        self._slider.sliderMoved.connect(self.sliderMoved)
        self._slider.sliderPressed.connect(self.sliderPressed)
        self._slider.sliderReleased.connect(self.sliderReleased)
        self._slider.valueChanged.connect(self.valueChanged)

        self._slider.valueChanged.connect(lambda x: self._label.setText(f"{x}"))

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._slider, Qt.AlignLeft)
        layout.addStretch()
        layout.addWidget(self._label)

    @pyqtSlot(int)
    def setValue(self, value: int) -> None:
        self._slider.setValue(value)
        self._label.setText(f"{value}")

    def value(self) -> int:
        return self._slider.value()

    @pyqtSlot(int, int)
    def setRange(self, a: int, b: int) -> None:
        self._slider.setRange(a, b)

    def setTickInterval(self, interval: int) -> None:
        self._slider.setTickInterval(interval)

    def setTickPosition(self, position: QSlider.TickPosition) -> None:
        self._slider.setTickPosition(position)

    def tickPosition(self) -> QSlider.TickPosition:
        return self._slider.tickPosition()

    def setMaximum(self, max: int) -> None:
        self._slider.setMaximum(max)

    def maximum(self) -> int:
        return self._slider.maximum()

    def setMinimum(self, max: int) -> None:
        self._slider.setMinimum(max)

    def minimum(self) -> int:
        return self._slider.minimum()
