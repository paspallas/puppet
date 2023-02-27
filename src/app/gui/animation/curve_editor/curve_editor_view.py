from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView

from ..items import TimeScaleItem


class CurveEditorView(QGraphicsView):
    def __init__(self) -> None:
        self._scene = QGraphicsScene(0, 0, 1200, 400)
        self._scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        super().__init__(self._scene)

        self.setContentsMargins(0, 0, 0, 0)
        self.setAlignment(Qt.AlignTop)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.WheelFocus)

        self.setOptimizationFlag(QGraphicsView.DontAdjustForAntialiasing)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.centerOn(0, 0)

        self._scale = TimeScaleItem(1200, self.fontMetrics())
        self._scene.addItem(self._scale)
