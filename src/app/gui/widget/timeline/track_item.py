import typing

import grid
from PyQt5.QtCore import QPointF, QRectF, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import (
    QGraphicsItem,
    QGraphicsObject,
    QStyleOptionGraphicsItem,
    QWidget,
)


class TrackItem(QGraphicsObject):
    sigCollapseChange = pyqtSignal(bool, int)

    def __init__(
        self,
        index: int,
        x: float = 0.0,
        y: float = 0.0,
        span: float = 200,
        color: QColor = QColor(Qt.white),
    ) -> None:
        super().__init__()
        self._index = index
        self._y = 0.0
        self._color = color
        self._collapsed = False
        self._rect = QRectF(0, 0, span, grid.__trackHeight__)
        self._expandedRect = QRectF(0, 0, span, grid.__trackHeight__)

        flags = (
            QGraphicsItem.ItemIsSelectable
            | QGraphicsItem.ItemIsMovable
            | QGraphicsItem.ItemSendsScenePositionChanges
        )
        self.setFlags(flags)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.setX(grid.__xoffset__ + x)
        self.setY(y)

    def addPropertyTrack(self, item: QGraphicsItem) -> None:
        childs = self.childItems()
        parentOffset = grid.__trackHeight__ + grid.__innerTrackSpacing__
        childOffset = grid.__trackHeight__ + grid.__subTrackVSpacing__

        if len(childs) > 0:
            item.setY(childs[-1].y() + childOffset)
        else:
            item.setY(parentOffset)

        item.setParentItem(self)

    def _computeExpandedRect(self) -> None:
        pass

    def expandedHeight(self) -> float:
        height = grid.__trackHeight__

        for i, _ in enumerate(self.childItems()):
            height += grid.__trackHeight__
            if i > 0:
                height += grid.__subTrackVSpacing__
            else:
                # first child
                height += grid.__innerTrackSpacing__

        return height

    def trackHeight(self) -> float:
        if self._collapsed:
            return grid.__trackHeight__

        return self.expandedHeight()

    def isCollapsed(self) -> bool:
        return self._collapsed

    def itemChange(
        self, change: QGraphicsItem.GraphicsItemChange, value: typing.Any
    ) -> typing.Any:
        if change == QGraphicsItem.ItemPositionChange and self.scene():
            return QPointF(grid.Grid.alignTo(value.x()), self._y)

        return super().itemChange(change, value)

    def setY(self, y: float) -> None:
        self._y = y
        super().setY(y)

    def boundingRect(self) -> QRectF:
        if self._collapsed:
            return self._rect

        return self._rect.adjusted(0, 0, 0, self.trackHeight() - grid.__trackHeight__)

    def mousePressEvent(self, e) -> None:
        if e.buttons() == Qt.LeftButton:
            self._collapsed = not self._collapsed
            self.sigCollapseChange.emit(self._collapsed, self._index)
        super().mousePressEvent(e)

    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget
    ) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self._color)
        painter.setPen(Qt.NoPen)

        if not self._collapsed:
            painter.save()
            painter.setOpacity(0.5)
            painter.drawRect(self.boundingRect())
            painter.restore()

        painter.setPen(Qt.black)
        painter.drawRect(self._rect)
