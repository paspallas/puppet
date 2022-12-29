from PyQt5.QtCore import QEvent, QObject, QPoint, Qt
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QGraphicsView, QStyleOptionGraphicsItem


class ZoomControl(QObject):
    """Add Zoom control with the mouse wheel to any QGraphicsView object

    Args:
        widget (QGraphicsView): The QGraphicsView we want to control
    """

    ZOOM_FACTOR = 1.2
    ZOOM_MAX = 40
    ZOOM_MIN = 0.75

    def __init__(self, widget: QGraphicsView = None):
        super().__init__(widget)

        widget.viewport().installEventFilter(self)

    def eventFilter(self, obj: QObject, e: QEvent) -> bool:
        view: QGraphicsView = obj.parent()

        if view is None:
            return super().eventFilter(obj, e)

        if e.type() == QEvent.Wheel:
            if e.modifiers() & Qt.Modifier.CTRL:
                lod = QStyleOptionGraphicsItem.levelOfDetailFromTransform(
                    view.transform()
                )

                if e.angleDelta().y() > 0:
                    if lod * self.ZOOM_FACTOR < self.ZOOM_MAX:
                        view.scale(self.ZOOM_FACTOR, self.ZOOM_FACTOR)
                    else:
                        view.scale(self.ZOOM_MAX / lod, self.ZOOM_MAX / lod)

                elif e.angleDelta().y() < 0:
                    if lod * (1 / self.ZOOM_FACTOR) > self.ZOOM_MIN:
                        view.scale(1 / self.ZOOM_FACTOR, 1 / self.ZOOM_FACTOR)
                    else:
                        view.scale(self.ZOOM_MIN / lod, self.ZOOM_MIN / lod)

                return True

        return super().eventFilter(obj, e)
