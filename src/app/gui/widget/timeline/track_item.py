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
        self._collapsed = True

        self._collapsedRect = QRectF(0, 0, span, grid.__trackHeight__)
        self._expandedRect = QRectF(0, 0, span, 0)
        self.childBoxHeight = 0.0

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

        if self._collapsed:
            item.setVisible(False)

        self._computeExpandedHeight()

    def trackHeight(self) -> float:
        if self._collapsed:
            return grid.__trackHeight__

        return self.childBoxHeight + grid.__trackHeight__

    def isCollapsed(self) -> bool:
        return self._collapsed

    def canExpand(self) -> bool:
        return len(self.childItems()) > 0

    def expand(self) -> None:
        if self.canExpand():
            self._collapsed = False
            self._updatePropertyTrackVisibility(True)
            self.sigCollapseChange.emit(False, self._index)

    def collapse(self) -> None:
        self._collapsed = True
        self._updatePropertyTrackVisibility(False)
        self.sigCollapseChange.emit(True, self._index)

    def changeState(self) -> None:
        if self._collapsed:
            self.expand()
        else:
            self.collapse()

    def _updatePropertyTrackVisibility(self, visible: bool) -> None:
        for child in self.childItems():
            child.setVisible(visible)

    def _computeExpandedHeight(self):
        height = 0

        for i, _ in enumerate(self.childItems()):
            height += grid.__trackHeight__
            if i > 0:
                height += grid.__subTrackVSpacing__
            else:
                # first child
                height += grid.__innerTrackSpacing__

        self._expandedRect.setHeight(height + grid.__trackHeight__)
        self.childBoxHeight = height

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
            return self._collapsedRect

        return self._expandedRect.adjusted(0, 0, 0, grid.__subTrackVSpacing__)

    def mousePressEvent(self, e) -> None:
        if e.buttons() == Qt.LeftButton:
            self.changeState()
        super().mousePressEvent(e)

    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget
    ) -> None:
        painter.setBrush(self._color)
        pen = QPen(Qt.black, 0, Qt.SolidLine)
        pen.setCosmetic(True)

        if self._collapsed:
            painter.setPen(pen)
            painter.drawRoundedRect(self._collapsedRect, 2, 2, Qt.AbsoluteSize)
        else:
            painter.setOpacity(0.5)
            painter.setPen(Qt.NoPen)
            painter.drawRect(
                self._expandedRect.adjusted(0, 0, 0, grid.__subTrackVSpacing__)
            )
            painter.setPen(pen)
            painter.setOpacity(1)
            painter.drawRect(self._collapsedRect)
