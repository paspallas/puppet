from PyQt5.QtCore import QObject, Qt, pyqtSlot
from PyQt5.QtWidgets import QAction, QMainWindow, QMenu, QMenuBar


class MainMenu(QObject):
    def __init__(self, parent: QMainWindow):
        super().__init__(parent)

        self._parent = parent
        self._menuBar = parent.menuBar()

        file_menu: QMenu = self._menuBar.addMenu("&File")
        edit_menu: QMenu = self._menuBar.addMenu("&Edit")
        view_menu: QMenu = self._menuBar.addMenu("&View")
        about_menu: QMenu = self._menuBar.addMenu("&About")

        file_menu.addAction("Save", lambda: print("saved"))
        file_menu.addAction("Open", lambda: print("open"))
        file_menu.addSeparator()

        file_quit = QAction("Quit", parent)
        file_quit.setShortcut("Ctrl+Q")
        file_quit.triggered.connect(self.quitApplication)
        file_menu.addAction(file_quit)

        view_timeline = parent._ui.animEditorDock.toggleViewAction()
        view_timeline.setShortcut("F1")
        view_menu.addAction(view_timeline)

        view_palette = parent._ui.spritePaletteDock.toggleViewAction()
        view_palette.setShortcut("F2")
        view_menu.addAction(view_palette)

        view_togglePropertyVisibility = QAction("Hide Sprite Properties", parent)
        view_togglePropertyVisibility.setCheckable(True)
        view_togglePropertyVisibility.setShortcut("F3")
        view_togglePropertyVisibility.triggered.connect(
            parent._ui.charEditor.toggleSpritePropertyVisibility
        )
        view_menu.addAction(view_togglePropertyVisibility)

        view_menu.addSeparator()
        view_fullscreen = QAction("Full Screen", parent)
        view_fullscreen.setCheckable(True)
        view_fullscreen.setShortcut("F11")
        view_fullscreen.triggered.connect(self.setfullScreen)
        view_menu.addAction(view_fullscreen)

    @pyqtSlot()
    def setfullScreen(self):
        if not self._parent.windowState() & Qt.WindowFullScreen:
            self._parent.setWindowState(Qt.WindowFullScreen)
        else:
            self._parent.setWindowState(Qt.WindowMaximized)

    @pyqtSlot()
    def quitApplication(self):
        self._parent.close()
