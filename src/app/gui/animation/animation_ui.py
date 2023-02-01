from PyQt5.QtWidgets import QPushButton, QListWidget, QHBoxLayout, QWidget


class AnimationUi:
    def setupUi(self, parent: QWidget) -> None:
        self.frameList = QListWidget(parent)
        self.addFrameBtn = QPushButton("+")

        box = QHBoxLayout(parent)
        box.addWidget(self.addFrameBtn)
        box.addWidget(self.frameList)
