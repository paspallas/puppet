from PyQt5.QtWidgets import QMainWindow

from .graphicview import GraphicView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._view = GraphicView(self)

        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("MegaPuppet")
        self.setMinimumSize(800, 600)
        self.setCentralWidget(self._view)
