import typing

from PyQt5.QtCore import QRectF, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QFontMetrics, QKeyEvent, QMouseEvent, QPainter, QWheelEvent
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsScene,
    QGraphicsView,
    QStyleOptionGraphicsItem,
    QWidget,
)

from .. import grid
from ..items import KeyFrameItem, PlayHeadItem, TimeScaleItem


class DopeSheetView(QGraphicsView):
    def __init__(self, parent: typing.Optional[QWidget] = None) -> None:
        self._scene = QGraphicsScene(0, 0, 1200, 400)
        self._scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        super().__init__(self._scene, parent)

        self.setAlignment(Qt.AlignTop)
        self.setStyleSheet("background-color: rgb(43, 42, 51);")

        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.WheelFocus)

        self.setOptimizationFlag(QGraphicsView.DontAdjustForAntialiasing)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.centerOn(0, 0)

        self._followPlayHead = True
        self.scalings = 0

        self._playHead = PlayHeadItem()
        self._scale = TimeScaleItem(self._scene.width())

        self._scene.addItem(self._playHead)
        self._scene.addItem(self._scale)

        self._scene.sceneRectChanged.connect(
            lambda rect: self._playHead.onSceneRectHeightChange(rect.height())
        )
        self._scene.sceneRectChanged.connect(
            lambda rect: self._scale.onAnimationLengthChanged
        )

        grid.Grid.computeGrid(self._scene.sceneRect(), [])

        self._makeConnections()

    def _makeConnections(self) -> None:
        self._playHead.sigPlayHeadPositionChange.connect(self.onPlayHeadPositionChange)
        self._playHead.sigPlayHeadPositionChange.connect(
            self._scale.onPlayHeadPositionChanged
        )
        self._scale.sigSetPlayHeadPosition.connect(self._playHead.setPlaybackPosition)
        self.verticalScrollBar().valueChanged.connect(
            self._playHead.onVerticalScrollBarChange
        )
        self.verticalScrollBar().valueChanged.connect(
            self._scale.onVerticalScrollBarChange
        )

    def drawBackground(self, painter: QPainter, rect: QRectF) -> None:
        grid.Grid.paint(painter)

    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.key() == Qt.Key_Q:
            self._playHead.rewind()
        elif e.key() == Qt.Key_E:
            self._playHead.advance()
        else:
            super().keyPressEvent(e)

    def wheelEvent(self, e: QWheelEvent) -> None:
        if e.modifiers() & Qt.Modifier.CTRL:
            degs = e.angleDelta().y() / 8
            steps = degs / 15
            self.scalings += steps

            if self.scalings * steps < 0:
                self.scalings = steps

            factor = 1.0 + (self.scalings / 160.0)
            self.scale(factor, 1.0)
        else:
            super().wheelEvent(e)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        if e.button() == Qt.MidButton:
            QApplication.setOverrideCursor(Qt.OpenHandCursor)
            self._start_pan_x = self.horizontalScrollBar().value() + e.x()
        else:
            super().mousePressEvent(e)

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        if (e.buttons() & Qt.MidButton) == Qt.MidButton:
            self.horizontalScrollBar().setValue(self._start_pan_x - e.x())
        else:
            super().mouseMoveEvent(e)

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        if e.button() == Qt.MidButton:
            QApplication.restoreOverrideCursor()
        super().mouseReleaseEvent(e)

    @pyqtSlot(bool)
    def setFollowPlayHead(self, follow: bool) -> None:
        self._followPlayHead = follow

    @pyqtSlot(float)
    def onPlayHeadPositionChange(self, pos: float) -> None:
        if self._scale.clicked:
            # don't scroll the view
            self._scale.clicked = False
            return

        if self._followPlayHead:
            self.centerOn(
                self._playHead.x(),
                self.mapToScene(self.viewport().rect()).boundingRect().center().y(),
            )
