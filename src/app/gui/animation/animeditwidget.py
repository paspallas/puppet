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


class AnimationEditorWidget(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self._frameList = QListWidget()
