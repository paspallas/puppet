from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon, QMouseEvent, QPaintEvent, QWheelEvent
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget

from ...resources import resources
from .. import style
from .doubleslider import DoubleSlider


class ZoomSlider(QWidget):
    zoomChanged = pyqtSignal(float)

    def __init__(self, *args, min_: float = 1, max_: float = 25, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setMaximumHeight(200)

        self.lupe = QLabel(self)
        self.lupe.setPixmap(QIcon(":/icon/32/lupe.png").pixmap(16, 16))

        self.slider = DoubleSlider(Qt.Orientation.Vertical, self)
        self.slider.setRange(min_, max_)
        self.slider.setValue(min_, False)

        vbox = QVBoxLayout(self)
        self.setLayout(vbox)
        vbox.addWidget(self.lupe)
        vbox.addWidget(self.slider)

        self.slider.valueChanged.connect(self.zoomChanged)

    @pyqtSlot(float)
    def setValue(self, value: float) -> None:
        self.slider.setValue(value, False)

    def paintEvent(self, e: QPaintEvent) -> None:
        style.paintWidget(self)

    def wheelEvent(self, e: QWheelEvent) -> None:
        self.slider.wheelEvent(e)
        e.accept()

    def mousePressEvent(self, e: QMouseEvent) -> None:
        self.slider.mousePressEvent(e)
        e.accept()
