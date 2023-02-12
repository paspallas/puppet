from PyQt5.QtCore import (
    QEasingCurve,
    QEvent,
    QObject,
    Qt,
    QTimeLine,
    pyqtSlot,
    pyqtSignal,
)
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QGraphicsView, QStyleOptionGraphicsItem


class ZoomControl(QObject):
    """Add Zoom control with the mouse wheel to any QGraphicsView

    Args:
        view (QGraphicsView): The view
        min_ (float): Minimum zoom level (defaults to 1)
        max_ (float): Maximum zoom level (defaults to 25)
    """

    zoomLevelChanged = pyqtSignal(float)

    def __init__(self, view: QGraphicsView, min_: float = 1, max_: float = 25):
        super().__init__(view)

        self._animation = QTimeLine(160, self)
        self._animation.setEasingCurve(QEasingCurve.InOutCubic)
        self._animation.setUpdateInterval(16)
        self._animation.valueChanged.connect(self.scalingTime)
        self._animation.finished.connect(self.animationFinished)
        self._numScalings = 0
        self._started = False

        self._view = view
        self._zoom_min = min_
        self._zoom_max = max_

        view.viewport().installEventFilter(self)

    def eventFilter(self, obj: QObject, e: QEvent) -> bool:
        view: QGraphicsView = obj.parent()

        if view is None:
            return super().eventFilter(obj, e)

        if e.type() == QEvent.Wheel:
            if e.modifiers() & (Qt.Modifier.CTRL | Qt.Modifier.ALT):
                return False

            self._numDegrees = e.angleDelta().y() / 8
            self._numSteps = self._numDegrees / 15
            self._numScalings += self._numSteps

            if self._numScalings * self._numSteps < 0:
                self._numScalings = self._numSteps

            if not self._started:
                self._started = True
                self._animation.start()

            return True

        return super().eventFilter(obj, e)

    def zoom(self) -> float:
        return round(
            QStyleOptionGraphicsItem.levelOfDetailFromTransform(self._view.transform()),
            4,
        )

    @pyqtSlot(float)
    def scalingTime(self, val: float) -> None:
        factor = 1.0 + (self._numScalings / 160.0)
        lod = self.zoom()
        level = lod * factor

        if self._zoom_min < level < self._zoom_max:
            self._view.scale(factor, factor)
            self.zoomLevelChanged.emit(level)
        elif level > self._zoom_max:
            self._view.scale(self._zoom_max / lod, self._zoom_max / lod)
            self._numScalings = 0
            self.zoomLevelChanged.emit(self._zoom_max)
        elif level < self._zoom_min:
            self._view.scale(self._zoom_min / lod, self._zoom_min / lod)
            self._numScalings = 0
            self.zoomLevelChanged.emit(self._zoom_min)

    @pyqtSlot(float)
    def setValue(self, value: float) -> None:
        # avoid recursion when a slider is connected to the controller
        if round(value, 4) == self.zoom():
            return

        transform = self._view.transform()
        m12 = transform.m12()  # Vertical shearing
        m13 = transform.m13()  # Horizontal Projection
        m21 = transform.m21()  # Horizontal shearing
        m23 = transform.m23()  # Vertical Projection
        m31 = transform.m31()  # Horizontal Position (DX)
        m32 = transform.m32()  # Vertical Position (DY)
        m33 = transform.m33()  # Additional Projection Factor

        transform.setMatrix(value, m12, m13, m21, value, m23, m31, m32, m33)
        self._view.setTransformationAnchor(QGraphicsView.AnchorViewCenter)
        self._view.setTransform(transform)
        self._view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    @pyqtSlot()
    def animationFinished(self) -> None:
        if self._numScalings > 0:
            self._numScalings -= 1
        else:
            self._numScalings += 1

        self._started = False
