from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QListView,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ...resources import resources


class AnimationUi:
    def setupUi(self, parent: QWidget) -> None:
        # control buttons
        self.playAnimationBtn = QPushButton(QIcon(":/icon/32/play.png"), "", parent)
        self.playAnimationBtn.setCheckable(True)
        self.playAnimationBtn.setToolTip("Play current animation")
        self.stopAnimationBtn = QPushButton(QIcon(":/icon/32/stop.png"), "", parent)
        self.stopAnimationBtn.setCheckable(True)
        self.stopAnimationBtn.setToolTip("Stop current animation")
        self.pauseAnimationBtn = QPushButton(QIcon(":/icon/32/pause.png"), "", parent)
        self.pauseAnimationBtn.setCheckable(True)
        self.pauseAnimationBtn.setToolTip("Pause current animation")

        ctrlBox = QHBoxLayout()
        ctrlBox.addStretch()
        ctrlBox.addWidget(self.playAnimationBtn)
        ctrlBox.addWidget(self.stopAnimationBtn)
        ctrlBox.addWidget(self.pauseAnimationBtn)
        ctrlBox.addStretch()

        # animations listview
        self.animationGroup = QGroupBox("Animations", parent)
        self.addAnimationBtn = QPushButton(QIcon(":/icon/16/add.png"), "", parent)
        self.addAnimationBtn.setToolTip("Add new animation")
        self.deleteAnimationBtn = QPushButton(QIcon(":/icon/16/delete.png"), "", parent)
        self.deleteAnimationBtn.setToolTip("Delete selected animation")
        self.animationList = QListView(parent)

        animBtnBox = QHBoxLayout()
        animBtnBox.addStretch()
        animBtnBox.addWidget(self.addAnimationBtn, 0, Qt.AlignRight)
        animBtnBox.addWidget(self.deleteAnimationBtn, 0, Qt.AlignRight)

        animVbox = QVBoxLayout(self.animationGroup)
        animVbox.addLayout(animBtnBox)
        animVbox.addWidget(self.animationList)

        # frames listview
        self.frameGroup = QGroupBox("Frames", parent)
        self.addFrameBtn = QPushButton(QIcon(":/icon/16/add.png"), "", parent)
        self.addFrameBtn.setToolTip("Set new frame")
        self.deleteFrameBtn = QPushButton(QIcon(":/icon/16/delete.png"), "", parent)
        self.deleteFrameBtn.setToolTip("Delete selected frame")
        self.frameList = QListView(parent)
        self.frameList.setFlow(QListView.LeftToRight)

        frameBtnBox = QHBoxLayout()
        frameBtnBox.addStretch()
        frameBtnBox.addWidget(self.addFrameBtn, 0, Qt.AlignRight)
        frameBtnBox.addWidget(self.deleteFrameBtn, 0, Qt.AlignRight)

        frameVbox = QVBoxLayout(self.frameGroup)
        frameVbox.addLayout(frameBtnBox)
        frameVbox.addWidget(self.frameList)

        # main container
        hbox = QHBoxLayout()
        hbox.addWidget(self.animationGroup, stretch=1)
        hbox.addWidget(self.frameGroup, stretch=3)

        container = QVBoxLayout(parent)
        container.addLayout(ctrlBox)
        container.addLayout(hbox)
