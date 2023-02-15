import typing

from PyQt5.QtCore import Qt, QPoint, QRect, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (
    QAbstractSlider,
    QLabel,
    QHBoxLayout,
    QSlider,
    QToolTip,
    QStyle,
    QStyleOptionSlider,
    QWidget,
)


class FancySlider(QWidget):
    actionTriggered = pyqtSignal(int)
    rangeChanged = pyqtSignal(int, int)
    sliderMoved = pyqtSignal(int)
    sliderPressed = pyqtSignal()
    sliderReleased = pyqtSignal()
    valueChanged = pyqtSignal(int)

    def __init__(
        self, orientation: Qt.Orientation, parent: typing.Optional[QWidget] = None
    ) -> None:
        super().__init__(parent)

        self._slider = QSlider(orientation)
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

    @pyqtSlot(int, int)
    def setRange(self, a: int, b: int) -> None:
        self._slider.setRange(a, b)

    @pyqtSlot(Qt.Orientation)
    def setOrientation(self, orientation: Qt.Orientation) -> None:
        self._slider.setOrientation(orientation)

    def setTickInterval(self, interval: int) -> None:
        self._slider.setTickInterval(interval)

    def setTickPosition(self, position: QSlider.TickPosition) -> None:
        self._slider.setTickPosition(position)

    def tickPosition(self) -> QSlider.TickPosition:
        return self._slider.tickPosition()

    def maximum(self) -> int:
        return self._slider.maximum()

    def minimum(self) -> int:
        return self._slider.minimum()

    def setMaximum(self, max: int) -> None:
        self._slider.setMaximum(max)

    def setMinimum(self, max: int) -> None:
        self._slider.setMinimum(max)


class FancySlider__(QSlider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def sliderChange(self, change: QAbstractSlider.SliderChange):
        super().sliderChange(change)

        if change == QAbstractSlider.SliderValueChange:
            opt = QStyleOptionSlider()
            self.initStyleOption(opt)

            rect = QRect(
                self.style().subControlRect(
                    QStyle.CC_Slider, opt, QStyle.SC_SliderHandle, self
                )
            )

            bottom_right_corner = rect.bottomLeft()
            QToolTip.showText(
                self.mapToGlobal(
                    QPoint(bottom_right_corner.x(), bottom_right_corner.y())
                ),
                str(self.value()),
                self,
            )
