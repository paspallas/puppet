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
    QGraphicsItem,
)

from ...model.sprite import Sprite, SpriteObject
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
        # TODO clean this mess
        self._ui_opacitySlide.valueChanged.connect(self.parent().handledItem.setOpacity)
        self._ui_flipHorizontalChk.stateChanged.connect(self.parent().handledItem.setHflip)
        self._ui_flipVerticalChk.stateChanged.connect(self.parent().handledItem.setVflip)
        
    def setOpacity(self, value: int) -> None:
        self._ui_opacitySlide.setValue(value)

    def setFlip(self, hflip: bool, vflip: bool) -> None:
        self._ui_flipHorizontalChk.setChecked(hflip)
        self._ui_flipVerticalChk.setChecked(vflip)


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

        self._properties = PropertiesGroupBox(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self._properties)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(self._ui_foregroundColor)
        painter.setBrush(self._ui_backgroundColor)
        rect = QRectF(
            QPoint(), QSizeF(self.size() - 0.5 * painter.pen().width() * QSize(1, 1))
        )
        painter.drawRoundedRect(rect, self._ui_borderRadius, self._ui_borderRadius)

    @pyqtSlot(QGraphicsItem)
    def sltOnSelectedItemChanged(self, item: QGraphicsItem):
        self.handledItem.setSpriteItem(item)

        # read current state of the item (viewmodel)
        # use signal, slots for this
        self._properties.setOpacity(item.opacity())
        self._properties.setFlip(item.hflip(), item.vflip())
