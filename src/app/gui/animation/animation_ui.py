from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHBoxLayout, QListView, QPushButton, QVBoxLayout, QWidget

from ...resources import resources


class AnimationUi:
    def setupUi(self, parent: QWidget) -> None:
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

        self.addAnimationBtn = QPushButton(QIcon(":/icon/16/add.png"), "", parent)
        self.addAnimationBtn.setToolTip("Add new animation")
        self.deleteAnimationBtn = QPushButton(QIcon(":/icon/16/delete.png"), "", parent)
        self.deleteAnimationBtn.setToolTip("Delete selected animation")

        btnBox = QVBoxLayout()
        btnBox.setDirection(QVBoxLayout.TopToBottom)
        btnBox.addWidget(self.addAnimationBtn, 0, Qt.AlignTop)
        btnBox.addWidget(self.deleteAnimationBtn, 0, Qt.AlignBottom)

        self.animationList = QListView(parent)
        self.frameList = QListView(parent)

        hbox = QHBoxLayout()
        hbox.addLayout(btnBox)
        hbox.addWidget(self.animationList, stretch=1)
        hbox.addWidget(self.frameList, stretch=3)

        container = QVBoxLayout(parent)
        container.addLayout(ctrlBox)
        container.addLayout(hbox)
