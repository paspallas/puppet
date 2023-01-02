from PyQt5.QtCore import QPoint, QRectF, QSize, QSizeF, Qt
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class RotateGroupBox(QGroupBox):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.setTitle("Tool Box")

        self.l_rotate = QSpinBox()
        self.l_rotate.setRange(0, 360)

        self.r_rotate = QSpinBox()
        self.r_rotate.setRange(0, 360)

        self.l_label = QLabel("left: ")
        self.r_label = QLabel("rigth: ")

        layout = QVBoxLayout(self)

        l1 = QHBoxLayout()
        l1.setContentsMargins(0, 0, 0, 0)
        l1.addWidget(self.l_label)
        l1.addWidget(self.l_rotate)

        l2 = QHBoxLayout()
        l2.setContentsMargins(0, 0, 0, 0)
        l2.addWidget(self.r_label)
        l2.addWidget(self.r_rotate)

        layout.addLayout(l1)
        layout.addLayout(l2)


class PropertyBox(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.background_color = QColor("salmon")
        self.foreground_color = QColor("red")
        self.border_radius = 10

        gr1 = RotateGroupBox()
        gr2 = RotateGroupBox()
        gr3 = RotateGroupBox()
        gr4 = RotateGroupBox()

        layout = QVBoxLayout(self)
        layout.addWidget(gr1)
        layout.addWidget(gr2)
        layout.addWidget(gr3)
        layout.addWidget(gr4)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(self.foreground_color)
        painter.setBrush(self.background_color)
        rect = QRectF(
            QPoint(), QSizeF(self.size() - 0.5 * painter.pen().width() * QSize(1, 1))
        )
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
