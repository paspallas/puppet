import typing

from PyQt5.QtCore import QPoint, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QMouseEvent, QWheelEvent
from PyQt5.QtWidgets import QSlider, QStyle, QStyleOptionSlider, QWidget


class DoubleSlider(QSlider):
    valueChanged = pyqtSignal(float)

    def __init__(self, orientation, parent: typing.Optional[QWidget] = None):
        super().__init__(orientation)

        self._decimals = 5
        self._maxInt = 10**self._decimals

        super().setMinimum(0)
        super().setMaximum(self._maxInt)
        super().valueChanged.connect(self._valueChanged)

        self._minValue = 0.0
        self._maxValue = 1.0

    @property
    def _valueRange(self) -> float:
        return self._maxValue - self._minValue

    def value(self) -> float:
        return self._intToFloat(super().value())

    @pyqtSlot(float, bool)
    def setValue(self, value: float, emit: bool = True) -> None:
        if emit:
            super().setValue(self._floatToInt(value))
        else:
            super().valueChanged.disconnect()
            super().setValue(self._floatToInt(value))
            super().valueChanged.connect(self._valueChanged)

    def _valueChanged(self, value: int) -> None:
        self.valueChanged.emit(self._intToFloat(value))

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

    def _pixelPosToRangeValue(self, pos: QPoint) -> float:
        opt = QStyleOptionSlider()
        self.initStyleOption(opt)
        gr = self.style().subControlRect(
            QStyle.CC_Slider, opt, QStyle.SC_SliderGroove, self
        )
        sr = self.style().subControlRect(
            QStyle.CC_Slider, opt, QStyle.SC_SliderHandle, self
        )

        if self.orientation() == Qt.Horizontal:
            sliderLength = sr.width()
            sliderMin = gr.x()
            sliderMax = gr.right() - sliderLength + 1
        else:
            sliderLength = sr.height()
            sliderMin = gr.y()
            sliderMax = gr.bottom() - sliderLength + 1

        pr = pos - sr.center() + sr.topLeft()
        p = pr.x() if self.orientation() == Qt.Horizontal else pr.y()

        value = QStyle.sliderValueFromPosition(
            super().minimum(),
            super().maximum(),
            p - sliderMin,
            sliderMax - sliderMin,
            opt.upsideDown,
        )

        return self._intToFloat(value)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        if e.button() == Qt.LeftButton:
            super().mousePressEvent(e)
            self.setValue(self._pixelPosToRangeValue(e.pos()))

    def wheelEvent(self, e: QWheelEvent):
        step = 0
        angle = e.angleDelta().y()
        if angle > 0:
            step = 1.5
        else:
            step = -1.5

        self.setValue(self.value() + step)
        e.accept()
