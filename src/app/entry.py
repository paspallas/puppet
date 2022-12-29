import sys

from PyQt5.QtWidgets import QApplication

from .gui.mainwindow import MainWindow


def start() -> None:
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())
