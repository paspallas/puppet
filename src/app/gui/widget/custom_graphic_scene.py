from typing import NamedTuple

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (
    QGraphicsItem,
    QGraphicsScene,
    QGraphicsSceneMouseEvent,
    QWidget,
)


class CustomGraphicSceneOptions(NamedTuple):
    width: int
    height: int


class CustomGraphicScene(QGraphicsScene):
    sigSelectedItem = pyqtSignal(QGraphicsItem)
    sigNoSelectedItem = pyqtSignal()

    def __init__(self, *args, options: CustomGraphicSceneOptions, **kwargs):
        super().__init__(*args, **kwargs)

        self.setSceneRect(
            -options.width // 2, -options.height // 2, options.width, options.height
        )

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
            self.sigNoSelectedItem.emit()

    def mousePressEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        super().mousePressEvent(e)

        if e.buttons() & Qt.LeftButton:
            item = self.itemAt(e.scenePos(), self.views()[0].transform())
            if item and item.flags() & QGraphicsItem.ItemIsSelectable:
                self.sigSelectedItem.emit(item)
