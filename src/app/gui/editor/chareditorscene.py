from PyQt5.QtCore import QPointF, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QGraphicsSceneMouseEvent

from ..widget import CustomGraphicScene, CustomGraphicSceneOptions


class CharEditorScene(CustomGraphicScene):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, options=CustomGraphicSceneOptions(2048, 2048, 32, True), **kwargs
        )

    def keyPressEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key.Key_Backspace:
            e.accept()

            items = self.selectedItems()

            for item in items:
                self.removeItem(item)
        else:
            super().keyPressEvent(e)
