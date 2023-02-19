import typing

from PyQt5.QtCore import QObject, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (
    QGraphicsItem,
    QGraphicsScene,
    QGraphicsSceneMouseEvent,
    QWidget,
)


class CustomGraphicScene(QGraphicsScene):
    sigSelectedItem = pyqtSignal(QGraphicsItem)
    sigNoItemSelected = pyqtSignal()

    def __init__(
        self, width: float, height: float, parent: typing.Optional[QObject] = None
    ) -> None:
        super().__init__(parent)

        self.setSceneRect(-width // 2, -height // 2, width, height)
        self.focusItemChanged.connect(self._onFocusItemChanged)

    @pyqtSlot(list)
    def addItems(self, items: typing.List[QGraphicsItem]) -> None:
        for item in items:
            self.addItem(item)

    @pyqtSlot(list)
    def delItems(self, items: typing.List[QGraphicsItem]) -> None:
        for item in items:
            self.removeItem(item)

    @pyqtSlot(QGraphicsItem, QGraphicsItem, Qt.FocusReason)
    def _onFocusItemChanged(
        self, new: QGraphicsItem, old: QGraphicsItem, reason: Qt.FocusReason
    ) -> None:
        if new is None:
            self.sigNoItemSelected.emit()
        else:
            self.sigSelectedItem.emit(new)
