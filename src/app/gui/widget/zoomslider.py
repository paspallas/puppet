from PyQt5.QtCore import QPoint, QRectF, QSize, QSizeF, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QColor, QIcon, QPainter, QPaintEvent, QPixmap, QWheelEvent
from PyQt5.QtWidgets import QLabel, QSlider, QVBoxLayout, QWidget

from ...resources import resources


class ZoomSlider(QWidget):
    zoomChanged = pyqtSignal(int)

    def __init__(self, *args, min_: int = 1, max_: int = 25, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setMaximumHeight(200)
        self.brushColor = QColor(66, 66, 66, 230)
        self.penColor = QColor("#424242")

        self.lupe = QLabel(self)
        self.lupe.setPixmap(QIcon(":/icon/32/lupe.png").pixmap(16, 16))

        self.zoomSlider = QSlider(Qt.Orientation.Vertical, self)
        self.zoomSlider.setRange(min_, max_)
        self.zoomSlider.setTickInterval(1)
        self.zoomSlider.setValue(min_)

        vbox = QVBoxLayout(self)
        self.setLayout(vbox)
        vbox.addWidget(self.lupe)
        vbox.addWidget(self.zoomSlider)

        self.zoomSlider.valueChanged.connect(self.zoomChanged)

    def paintEvent(self, e: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(self.penColor)
        painter.setBrush(self.brushColor)
        rect = QRectF(
            QPoint(), QSizeF(self.size() - 0.5 * painter.pen().width() * QSize(1, 1))
        )
        painter.drawRoundedRect(rect, 10, 10)

    def wheelEvent(self, event: QWheelEvent) -> None:
        self.zoomSlider.wheelEvent(event)
        event.accept()
