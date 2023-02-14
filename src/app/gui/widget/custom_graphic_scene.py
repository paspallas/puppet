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

    def __init__(self, *args, options: CustomGraphicSceneOptions, **kwargs):
        super().__init__(*args, **kwargs)

        self.activeItem = None
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
        if item:
            print(item)
            self.sigSelectedItem.emit(item)

    # def mousePressEvent(self, e: QGraphicsSceneMouseEvent) -> None:
    #     super().mousePressEvent(e)

    #     if e.buttons() & Qt.LeftButton:
    #         self.activeItem = self.itemAt(e.scenePos(), self.views()[0].transform())
    #         if self.activeItem:
    #             if self.activeItem.flags() & QGraphicsItem.ItemIsSelectable:
    #                 self.sigSelectedItem.emit(self.activeItem)
    #                 print(self.activeItem)

    # elif e.buttons() & Qt.RightButton:
    #     self.renderFrame()
