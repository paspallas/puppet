from PyQt5.QtCore import QPoint, QRectF, QSize, QSizeF, Qt, pyqtSlot
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QVBoxLayout,
    QWidget,
    QSlider,
)

from app.model.sprite import SpriteObject, Sprite


class PropertiesGroupBox(QGroupBox):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.setTitle("Sprite Properties")

        self.opacity = QSlider()
        self.opacity.setRange(0, 100)
        self.opacity.setValue(100)
        self.opacity.setOrientation(Qt.Horizontal)

        # self.l_rotate = QSpinBox()
        # self.l_rotate.setRange(0, 360)

        # self.r_rotate = QSpinBox()
        # self.r_rotate.setRange(0, 360)

        self.opacity_label = QLabel("opacity: ")
        # self.r_label = QLabel("rigth: ")

        layout = QVBoxLayout(self)

        l1 = QHBoxLayout()
        l1.setContentsMargins(0, 0, 0, 0)
        l1.addWidget(self.opacity_label)
        l1.addWidget(self.opacity)

        # l2 = QHBoxLayout()
        # l2.setContentsMargins(0, 0, 0, 0)
        # l2.addWidget(self.r_label)
        # l2.addWidget(self.r_rotate)

        layout.addLayout(l1)
        # layout.addLayout(l2)

        self.makeConnections()

    def makeConnections(self):
        self.opacity.valueChanged.connect(self.parent().handledItem.setOpacity)


class PropertyBox(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.background_color = QColor("#424242")
        self.foreground_color = QColor("#353535")
        self.border_radius = 4

        self.handledItem = SpriteObject()

        gr1 = PropertiesGroupBox(self)
        # gr2 = RotateGroupBox()
        # gr3 = RotateGroupBox()
        # gr4 = RotateGroupBox()

        layout = QVBoxLayout(self)
        layout.addWidget(gr1)
        # layout.addWidget(gr2)
        # layout.addWidget(gr3)
        # layout.addWidget(gr4)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(self.foreground_color)
        painter.setBrush(self.background_color)
        rect = QRectF(
            QPoint(), QSizeF(self.size() - 0.5 * painter.pen().width() * QSize(1, 1))
        )
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)

    @pyqtSlot(Sprite)
    def onSelectedItemChanged(self, item: Sprite):
        print("on sprite changed")
        self.handledItem.setSpriteItem(item)
