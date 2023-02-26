from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction, QMainWindow

from ..model.document import Document
from .app_window_ui import EditModeUi
from .menu.main_menu import MainMenu


class AppWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Puppet Studio")
        self.setMinimumSize(1280, 800)
        self.setFocusPolicy(Qt.StrongFocus)

        self._ui = EditModeUi()
        self._ui.setupUi(self)
        self.setupActions()
        self._menu = MainMenu(self)

        self._document = Document()

        self._ui.charEditor.setDocument(self._document)
        self._ui.spritePaletteDock.setDocument(self._document)
        # self._ui.animEditorDock.setDocument(self._document)

    def setupActions(self):
        # enable the control of the dopesheet with keyboard shorcuts
        # regardless of its focus state

        self.advance = QAction("advance")
        self.advance.setShortcut("E")
        self.advance.triggered.connect(self._ui.animEditorDock.advance)

        self.rewind = QAction("rewind")
        self.rewind.setShortcut("Q")
        self.rewind.triggered.connect(self._ui.animEditorDock.rewind)

        self.keyframe = QAction("keyframe")
        self.keyframe.setShortcut("Space")
        self.keyframe.triggered.connect(self._ui.animEditorDock.setKeyframe)

        self.addActions([self.advance, self.rewind, self.keyframe])
