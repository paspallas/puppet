from PyQt5.QtCore import QPoint, QRectF, QSize, QSizeF, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import (
    QColor,
    QIcon,
    QMouseEvent,
    QPainter,
    QPaintEvent,
    QPixmap,
    QWheelEvent,
)
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget

from ...resources import resources
from .doubleslider import DoubleSlider


class ZoomSlider(QWidget):
    zoomChanged = pyqtSignal(float)

    def __init__(self, *args, min_: float = 1, max_: float = 25, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setMaximumHeight(200)
        self.brushColor = QColor(66, 66, 66, 230)
        self.penColor = QColor("#424242")

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
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(self.penColor)
        painter.setBrush(self.brushColor)
        rect = QRectF(
            QPoint(), QSizeF(self.size() - 0.5 * painter.pen().width() * QSize(1, 1))
        )
        painter.drawRoundedRect(rect, 10, 10)

    def wheelEvent(self, e: QWheelEvent) -> None:
        self.slider.wheelEvent(e)
        e.accept()

    def mousePressEvent(self, e: QMouseEvent) -> None:
        e.accept()
