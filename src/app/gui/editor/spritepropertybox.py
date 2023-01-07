from PyQt5.QtCore import QPoint, QRectF, QSize, QSizeF, Qt, pyqtSlot
from PyQt5.QtGui import QColor, QPainter, QPaintEvent
from PyQt5.QtWidgets import (
    QCheckBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from app.model.sprite import Sprite, SpriteObject

from ..widget import ColorButton, FancySlider


class PropertiesGroupBox(QGroupBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setTitle("Sprite Properties")
        self.__setupUi()
        self.__makeConnections()

    def __setupUi(self):
        self._ui_opacitySlide = FancySlider()
        self._ui_opacitySlide.setRange(0, 100)
        self._ui_opacitySlide.setValue(100)
        self._ui_opacitySlide.setOrientation(Qt.Horizontal)

        self._ui_opacityLbl = QLabel("Opacity: ")

        self._ui_colorBtn = ColorButton()
        self._ui_colorLbl = QLabel("Tint: ")

        self._ui_flipVerticalChk = QCheckBox("Flip Vertical")
        self._ui_flipHorizontalChk = QCheckBox("Flip Horizontal")

        h1 = QHBoxLayout()
        h1.addWidget(self._ui_opacityLbl, stretch=1)
        h1.addWidget(self._ui_opacitySlide, stretch=3)

        h2 = QHBoxLayout()
        h2.addWidget(self._ui_colorLbl, stretch=1)
        h2.addWidget(self._ui_colorBtn, stretch=3)

        h3 = QHBoxLayout()
        h3.addWidget(self._ui_flipHorizontalChk)
        h3.addWidget(self._ui_flipVerticalChk)

        vbox = QVBoxLayout(self)
        vbox.addLayout(h1)
        vbox.addLayout(h2)
        vbox.addLayout(h3)

    def __makeConnections(self):
        self._ui_opacitySlide.valueChanged.connect(self.parent().handledItem.setOpacity)


class SpritePropertyBox(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setMinimumSize(QSize(250, 64))

        self._ui_backgroundColor = QColor("#424242")
        self._ui_foregroundColor = QColor("#353535")
        self._ui_borderRadius = 4

        self.handledItem = SpriteObject()

        gr1 = PropertiesGroupBox(self)
        layout = QVBoxLayout(self)
        layout.addWidget(gr1)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(self._ui_foregroundColor)
        painter.setBrush(self._ui_backgroundColor)
        rect = QRectF(
            QPoint(), QSizeF(self.size() - 0.5 * painter.pen().width() * QSize(1, 1))
        )
        painter.drawRoundedRect(rect, self._ui_borderRadius, self._ui_borderRadius)

    @pyqtSlot(Sprite)
    def sltOnSelectedItemChanged(self, item: Sprite):
        print("on sprite changed")
        self.handledItem.setSpriteItem(item)
