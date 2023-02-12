import typing

from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QSlider, QWidget


class DoubleSlider(QSlider):
    valueChanged = pyqtSignal(float)

    def __init__(self, orientation, parent: typing.Optional[QWidget] = None):
        super().__init__(orientation)

        self._decimals = 6
        self._maxInt = 10**self._decimals

        super().setMinimum(0)
        super().setMaximum(self._maxInt)
        super().valueChanged.connect(
            lambda x: self.valueChanged.emit(self._intToFloat(x))
        )

        self._minValue = 0.0
        self._maxValue = 1.0

    @property
    def _valueRange(self) -> float:
        return self._maxValue - self._minValue

    def value(self) -> float:
        return self._intToFloat(super().value())

    @pyqtSlot(float)
    def setValue(self, value: float) -> None:
        super().setValue(self._floatToInt(value))

    def setMinimum(self, value: float) -> None:
        if value > self._maxValue:
            raise ValueError("Minimum limit cannot be higher than maximum limit")

        self._minValue = value

    def setMaximum(self, value: float) -> None:
        if value < self._minValue:
            raise ValueError("Maximum limit cannot be lower that minimum limit")

        self._maxValue = value

    def setRange(self, min: float, max: float) -> None:
        self.setMaximum(max)
        self.setMinimum(min)

    def minimum(self) -> float:
        return self._minValue

    def maximum(self) -> float:
        return self._maxValue

    def _floatToInt(self, value: float) -> int:
        return int(((value - self._minValue) / self._valueRange) * self._maxInt)

    def _intToFloat(self, value: int) -> float:
        return ((float(value) / self._maxInt) * self._valueRange) + self._minValue
