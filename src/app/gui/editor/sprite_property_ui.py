from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QCheckBox,
    QDoubleSpinBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ...resources import resources
from ..widget import FancySlider


class SpritePropertyUi:
    def setupUi(self, parent: QWidget) -> None:
        self.xSpin = QDoubleSpinBox()
        self.xSpin.setMinimum(-9999)
        self.xSpin.setMaximum(9999)
        self.xLbl = QLabel("x")
        self.xLbl.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.xLbl.setBuddy(self.xSpin)

        self.ySpin = QDoubleSpinBox()
        self.ySpin.setMinimum(-9999)
        self.ySpin.setMaximum(9999)
        self.yLbl = QLabel("y")
        self.yLbl.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.yLbl.setBuddy(self.ySpin)

        self.opacitySlide = FancySlider(Qt.Horizontal)
        self.opacitySlide.setRange(0, 100)
        self.opacitySlide.setValue(0)
        self.opacityLbl = QLabel("Alpha")
        self.opacityLbl.setBuddy(self.opacitySlide)

        self.flipVerticalChk = QCheckBox("Vertical")
        self.flipHorizontalChk = QCheckBox("Horizontal")
        self.flipLabel = QLabel("Flip")

        h0 = QHBoxLayout()
        h0.addWidget(self.opacityLbl, stretch=1)
        h0.addWidget(self.opacitySlide, stretch=3)

        h1 = QHBoxLayout()
        self.posLbl = QLabel("Position")
        h1.addWidget(self.posLbl)
        h1.addWidget(self.xLbl, stretch=1)
        h1.addWidget(self.xSpin, stretch=2)
        h1.addWidget(self.yLbl, stretch=1)
        h1.addWidget(self.ySpin, stretch=2)

        h2 = QHBoxLayout()
        h2.addWidget(self.flipLabel)
        h2.addWidget(self.flipHorizontalChk, 0)
        h2.addWidget(self.flipVerticalChk, 0)

        propertyBoxLay = QVBoxLayout()
        propertyBoxLay.addLayout(h0)
        propertyBoxLay.addLayout(h1)
        propertyBoxLay.addLayout(h2)

        self.propertyBox = QGroupBox("Properties", parent)
        self.propertyBox.setLayout(propertyBoxLay)

        vbox = QVBoxLayout(parent)
        vbox.addWidget(self.propertyBox)
