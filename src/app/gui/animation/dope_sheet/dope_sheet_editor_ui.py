import typing

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
)

from .dope_sheet_view import DopeSheetView


class DopeSheetEditorUi:
    def setupUi(self, parent: QWidget) -> None:
        parent.setMinimumWidth(800)

        self.dopeSheetView = DopeSheetView()
        self.dopeSheetView.setStyleSheet("background-color: rgb(60, 60, 60);")

        vbox = QVBoxLayout(parent)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(self.dopeSheetView)
