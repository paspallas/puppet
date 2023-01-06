from PyQt5.QtCore import QPoint, Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QMouseEvent
from PyQt5.QtWidgets import QFrame, QGraphicsView, QSizePolicy, QWidget

from app.model.sprite import Sprite

from .graphicscene import GraphicScene
from .viewcontrol import PanControl, ZoomControl


class GraphicView(QGraphicsView):
    selectedItemChanged = pyqtSignal(Sprite)

    def __init__(self, parent: QWidget, scene: GraphicScene):
        super().__init__(scene, parent)

        self._widgets = dict()

        PanControl(self)
        ZoomControl(self)

        self._setup()

    def _setup(self) -> None:
        self.setFrameStyle(QFrame.NoFrame)
        self.setContentsMargins(0, 0, 0, 0)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setMouseTracking(True)

    def addFixedWidget(self, widget: QWidget, aligment):
        widget.setParent(self.viewport())
        self._widgets[widget] = aligment

    def showEvent(self, event):
        self._updateFixedWidgets()
        super().showEvent(event)

    def resizeEvent(self, event):
        self._updateFixedWidgets()
        super().resizeEvent(event)

    def _updateFixedWidgets(self):
        r = self.viewport().rect()

        for w, a in self._widgets.items():
            p = QPoint()

            if a & Qt.AlignCenter:
                p.setX(int((r.width() - w.width()) / 2))
            elif a & Qt.AlignRight:
                p.setX(int(r.width() - w.width() - 2))
            elif a & Qt.AlignLeft:
                p.setX(p.x() + 2)

            if a & Qt.AlignVCenter:
                p.setY(int((r.height() - w.height()) / 2))
            elif a & Qt.AlignBottom:
                p.setY(r.height() - w.height() - 2)
            elif a & Qt.AlignTop:
                p.setY(p.y() + 2)

            w.move(p)

    def mousePressEvent(self, e: QMouseEvent):
        selected_sprite = self.itemAt(e.pos())

        if isinstance(selected_sprite, Sprite):
            self.selectedItemChanged.emit(selected_sprite)
            print("sprite_changed")

        super().mousePressEvent(e)
