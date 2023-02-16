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

        self.selectionChanged.connect(self._onSelectionChanged)

    @pyqtSlot(list)
    def addItems(self, items: list[QGraphicsItem]) -> None:
        for item in items:
            self.addItem(item)

    @pyqtSlot(list)
    def delItems(self, items: list[QGraphicsItem]) -> None:
        for item in items:
            self.removeItem(item)

    @pyqtSlot()
    def _onSelectionChanged(self) -> None:
        item = self.mouseGrabberItem()
        if item is None:
            self.sigNoItemSelected.emit()

    def mousePressEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        super().mousePressEvent(e)

        if e.buttons() & Qt.LeftButton:
            item = self.itemAt(e.scenePos(), self.views()[0].transform())
            if item and item.flags() & QGraphicsItem.ItemIsSelectable:
                self.sigSelectedItem.emit(item)
