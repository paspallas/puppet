from PyQt5.QtWidgets import QMainWindow

from ..model.chardocument import CharDocument
from .appwindow_ui import EditModeUi
from .menu.main_menu import MainMenu


class AppWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Puppet Studio")
        self.setMinimumSize(1280, 800)

        self._ui = EditModeUi()
        self._ui.setupUi(self)
        self._menu = MainMenu(self)

        self._document = CharDocument()

        self._ui.charEditor.setDocument(self._document)
        self._ui.spritePaletteDock.setDocument(self._document)
        self._ui.animEditorDock.setDocument(self._document)
