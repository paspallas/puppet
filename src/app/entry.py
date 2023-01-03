import sys

import qtmodern.styles
import qtmodern.windows
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QStyleFactory

from .gui.mainwindow import MainWindow

try:
    from PyQt5.QtWinExtras import QtWin

    QtWin.setCurrentProcessExplicitAppUserModelID("com.paspallas.tool.puppet")
except ImportError:
    pass


def start() -> None:
    QApplication.setStyle(QStyleFactory.create("Fusion"))
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    app = QApplication([])
    qtmodern.styles.dark(app)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())
