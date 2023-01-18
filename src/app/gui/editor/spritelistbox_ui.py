from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTreeView,
    QVBoxLayout,
    QWidget,
)

from ...resources import resources
from ..widget import ColorButton, FancySlider


class SpriteListBoxUi:
    def setupUi(self, parent: QWidget):
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

        self.flipVerticalChk = QCheckBox("Flip Vertical")
        self.flipHorizontalChk = QCheckBox("Flip Horizontal")

        h1 = QHBoxLayout()
        h1.addWidget(self.opacityLbl, stretch=1)
        h1.addWidget(self.opacitySlide, stretch=3)

        h2 = QHBoxLayout()
        h2.addWidget(self.colorLbl, stretch=1)
        h2.addWidget(self.colorBtn, stretch=3)

        h3 = QHBoxLayout()
        h3.addStretch()
        h3.addWidget(self.flipHorizontalChk, 0)
        h3.addWidget(self.flipVerticalChk, 0)
        h3.addStretch()

        vbox1 = QVBoxLayout()
        vbox1.setSpacing(10)
        vbox1.addLayout(h1)
        vbox1.addLayout(h2)
        vbox1.addLayout(h3)

        self.propertyBox = QGroupBox("Sprite Properties", parent)
        self.propertyBox.setLayout(vbox1)

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

        self.upBtn = QPushButton(QIcon(":/icon/16/up.png"), "")
        self.downBtn = QPushButton(QIcon(":/icon/16/down.png"), "")
        self.delBtn = QPushButton(QIcon(":/icon/16/delete.png"), "")

        btnBox = QHBoxLayout()
        btnBox.addWidget(self.upBtn, 0, Qt.AlignLeft)
        btnBox.addWidget(self.downBtn, 0, Qt.AlignLeft)
        btnBox.addStretch()
        btnBox.addWidget(self.delBtn, 0, Qt.AlignRight)

        vbox2 = QVBoxLayout(parent)
        vbox2.addWidget(self.propertyBox)
        vbox2.addWidget(self.list)
        vbox2.addLayout(btnBox)
