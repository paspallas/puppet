from PyQt5.QtCore import QPoint, QRectF, QSize, QSizeF, Qt, pyqtSlot
from PyQt5.QtGui import QColor, QPainter, QPaintEvent
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QSizePolicy,
    QSlider,
    QSpacerItem,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class FancySlider(QSlider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
