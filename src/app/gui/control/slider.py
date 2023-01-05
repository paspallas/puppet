from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtWidgets import (
    QAbstractSlider,
    QSlider,
    QToolTip,
    QStyle,
    QStyleOptionSlider,
)


class FancySlider(QSlider):
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
