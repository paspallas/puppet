from PyQt5.QtCore import QPoint, QRectF, QSize, QSizeF, Qt, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QBrush, QColor, QPainter, QPixmap, QMouseEvent
from PyQt5.QtWidgets import (
    QBoxLayout,
    QDockWidget,
    QFrame,
    QGraphicsItem,
    QGraphicsItemGroup,
    QGraphicsScene,
    QGraphicsView,
    QHBoxLayout,
    QListWidget,
    QMainWindow,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from ...model.chardocument import CharDocument


class AnimationEditorDock(QDockWidget):
    def __init__(self, *args, model: CharDocument, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Timeline")
        self.setAllowedAreas(Qt.BottomDockWidgetArea)

        self._container = QWidget(self)
        self.setWidget(self._container)

        self._model = model
