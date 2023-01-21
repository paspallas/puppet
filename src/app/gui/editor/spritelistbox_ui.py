from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QSpinBox,
    QTreeView,
    QVBoxLayout,
    QWidget,
)

from ...resources import resources
from ..widget import ColorButton, FancySlider


class SpriteListBoxUi:
    def setupUi(self, parent: QWidget):

        self.brushColor = QColor("#424242")
        self.penColor = QColor("#424242")

        self.xSpin = QSpinBox()
        self.xSpin.setMinimum(-9999)
        self.xSpin.setMaximum(9999)
        self.xLbl = QLabel("X: ")
        self.xLbl.setBuddy(self.xSpin)

        self.ySpin = QSpinBox()
        self.ySpin.setMinimum(-9999)
        self.ySpin.setMaximum(9999)
        self.yLbl = QLabel("Y: ")
        self.yLbl.setBuddy(self.ySpin)

        self.opacitySlide = FancySlider()
        self.opacitySlide.setRange(0, 100)
        self.opacitySlide.setValue(100)
        self.opacitySlide.setTickInterval(1)
        self.opacitySlide.setOrientation(Qt.Horizontal)
        self.opacityLbl = QLabel("Opacity: ")
        self.opacityLbl.setBuddy(self.opacitySlide)

        self.colorBtn = ColorButton()
        self.colorLbl = QLabel("Tint: ")
        self.colorLbl.setBuddy(self.colorBtn)

        self.flipVerticalChk = QCheckBox("Vertical")
        self.flipHorizontalChk = QCheckBox("Horizontal")
        self.flipLabel = QLabel("Flip: ")

        h0 = QHBoxLayout()
        h0.addWidget(self.opacityLbl, stretch=1)
        h0.addWidget(self.opacitySlide, stretch=3)

        h1 = QHBoxLayout()
        h1.addWidget(self.colorLbl, stretch=1)
        h1.addWidget(self.colorBtn, stretch=3)

        h2 = QHBoxLayout()
        h2.addWidget(self.xLbl, stretch=1)
        h2.addWidget(self.xSpin, stretch=3)

        h3 = QHBoxLayout()
        h3.addWidget(self.yLbl, stretch=1)
        h3.addWidget(self.ySpin, stretch=3)

        h4 = QHBoxLayout()
        h4.addWidget(self.flipLabel)
        h4.addWidget(self.flipHorizontalChk, 0)
        h4.addWidget(self.flipVerticalChk, 0)

        propertyBoxLay = QVBoxLayout()
        propertyBoxLay.addLayout(h0)
        propertyBoxLay.addLayout(h1)
        propertyBoxLay.addLayout(h2)
        propertyBoxLay.addLayout(h3)
        propertyBoxLay.addLayout(h4)

        self.propertyBox = QGroupBox("Properties", parent)
        self.propertyBox.setLayout(propertyBoxLay)

        self.list = QTreeView(parent)
        self.list.setRootIsDecorated(False)
        self.list.setDragEnabled(True)
        self.list.setAcceptDrops(True)
        self.list.setDragDropOverwriteMode(False)
        self.list.setDragDropMode(QAbstractItemView.DragDrop)
        self.list.setDropIndicatorShown(True)
        self.list.setDefaultDropAction(Qt.MoveAction)
        self.list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.list.setHeaderHidden(True)
        self.list.header().setStretchLastSection(False)

        self.upBtn = QPushButton(QIcon(":/icon/16/up.png"), "")
        self.downBtn = QPushButton(QIcon(":/icon/16/down.png"), "")
        self.delBtn = QPushButton(QIcon(":/icon/16/delete.png"), "")

        btnBox = QHBoxLayout()
        btnBox.addWidget(self.upBtn, 0, Qt.AlignLeft)
        btnBox.addWidget(self.downBtn, 0, Qt.AlignLeft)
        btnBox.addStretch()
        btnBox.addWidget(self.delBtn, 0, Qt.AlignRight)

        spriteListLay = QVBoxLayout()
        spriteListLay.addWidget(self.list)
        spriteListLay.addLayout(btnBox)

        self.spriteListBox = QGroupBox("Sprites", parent)
        self.spriteListBox.setLayout(spriteListLay)

        layout = QVBoxLayout(parent)
        layout.addWidget(self.propertyBox)
        layout.addWidget(self.spriteListBox)

    def updateHeaders(self) -> None:
        """Update header size policy after the model has been set"""
        self.list.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.list.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.list.header().setSectionResizeMode(2, QHeaderView.ResizeToContents)
