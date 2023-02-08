from PyQt5.QtCore import QEasingCurve, QEvent, QObject, Qt, QTimeLine, pyqtSlot
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QGraphicsView, QStyleOptionGraphicsItem


class ZoomControl(QObject):
    """Add Zoom control with the mouse wheel to any QGraphicsView

    Args:
        view (QGraphicsView): The view
    """

    ZOOM_MAX = 25
    ZOOM_MIN = 1

    def __init__(self, view: QGraphicsView):
        super().__init__(view)

        self._animation = QTimeLine(160, self)
        self._animation.setEasingCurve(QEasingCurve.InOutCubic)
        self._animation.setUpdateInterval(16)
        self._animation.valueChanged.connect(self.scalingTime)
        self._animation.finished.connect(self.animationFinished)
        self._numScalings = 0
        self._started = False

        self._view = view

        view.viewport().installEventFilter(self)

    def eventFilter(self, obj: QObject, e: QEvent) -> bool:
        view: QGraphicsView = obj.parent()

        if view is None:
            return super().eventFilter(obj, e)

        if e.type() == QEvent.Wheel:
            if e.modifiers() & Qt.Modifier.CTRL:
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

    @pyqtSlot(float)
    def scalingTime(self, val: float) -> None:
        lod = QStyleOptionGraphicsItem.levelOfDetailFromTransform(
            self._view.transform()
        )
        factor = 1.0 + (self._numScalings / 160.0)

        nextLod = lod * factor

        if self.ZOOM_MIN < nextLod < self.ZOOM_MAX:
            self._view.scale(factor, factor)
        elif nextLod > self.ZOOM_MAX:
            self._view.scale(self.ZOOM_MAX / lod, self.ZOOM_MAX / lod)
            self._numScalings = 0
        elif nextLod < self.ZOOM_MIN:
            self._view.scale(self.ZOOM_MIN / lod, self.ZOOM_MIN / lod)
            self._numScalings = 0

    @pyqtSlot()
    def animationFinished(self) -> None:
        if self._numScalings > 0:
            self._numScalings -= 1
        else:
            self._numScalings += 1

        self._started = False
