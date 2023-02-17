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

    @pyqtSlot(list)
    def addItems(self, items: typing.List[QGraphicsItem]) -> None:
        for item in items:
            self.addItem(item)

    @pyqtSlot(list)
    def delItems(self, items: typing.List[QGraphicsItem]) -> None:
        for item in items:
            self.removeItem(item)

    def mousePressEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        super().mousePressEvent(e)

        if e.buttons() & Qt.LeftButton:
            item = self.itemAt(e.scenePos(), self.views()[0].transform())
            if item:
                if item.flags() & QGraphicsItem.ItemIsSelectable:
                    self.sigSelectedItem.emit(item)
            else:
                self.sigNoItemSelected.emit()
