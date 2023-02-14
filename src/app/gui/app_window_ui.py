from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QTabWidget

from .animation import AnimationEditorDock
from .editor import CharEditorWidget
from .palette import SpritePaletteDock


class EditModeUi:
    def setupUi(self, parent: QMainWindow):
        self.charEditor = CharEditorWidget(parent)
        self.spritePaletteDock = SpritePaletteDock(parent)
        self.animEditorDock = AnimationEditorDock(parent)

        parent.setCentralWidget(self.charEditor)

        parent.setTabPosition(Qt.BottomDockWidgetArea, QTabWidget.South)
        parent.setTabShape(QTabWidget.Rounded)
        parent.addDockWidget(Qt.BottomDockWidgetArea, self.spritePaletteDock)
        parent.addDockWidget(Qt.BottomDockWidgetArea, self.animEditorDock)
        parent.tabifyDockWidget(self.spritePaletteDock, self.animEditorDock)

        self.spritePaletteDock.hide()
        self.animEditorDock.hide()
