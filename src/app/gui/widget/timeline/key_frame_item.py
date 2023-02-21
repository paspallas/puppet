import typing
from enum import IntEnum

import grid
from PyQt5.QtCore import QPointF, QRectF, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import (
    QGraphicsItem,
    QGraphicsObject,
    QGraphicsSceneHoverEvent,
    QGraphicsSceneMouseEvent,
    QStyleOptionGraphicsItem,
    QWidget,
)


class Rect(IntEnum):
    Left = 0
    Right = 1


class KeyFrameItem(QGraphicsObject):
    __selectedColor__ = QColor(Qt.cyan)
    __normalColor__ = QColor(Qt.magenta)
    __controlRectWidth__ = 2
    __controlRectHeight__ = grid.__height__

    sigTrackDurationChanged = pyqtSignal(float)

    def __init__(self, x: float, y: float, w: float, h: float) -> None:
        super().__init__()

        self._rect = QRectF(0, 0, w, h)
        self.setX(x)
        self.setY(y)

        flags = (
            QGraphicsItem.ItemIsSelectable
            | QGraphicsItem.ItemIsMovable
            | QGraphicsItem.ItemSendsGeometryChanges
            | QGraphicsItem.ItemSendsScenePositionChanges
        )

        self.setFlags(flags)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.setZValue(-1)
        self.setAcceptHoverEvents(True)

        self._leftControlRect = QRectF(
            0, 0, self.__controlRectWidth__, self.__controlRectHeight__
        )
        self._rightControlRect = QRectF(
            w - self.__controlRectWidth__,
            0,
            self.__controlRectWidth__,
            self.__controlRectHeight__,
        )

        self._selectedCtrlRect = None
        self._resizeOrigin = 0.0
        self._isResizing = False

    def boundingRect(self) -> QRectF:
        return self._rect

    def insideControlRects(self, pos: QPointF) -> bool:
        if self._leftControlRect.contains(pos):
            self._selectedCtrlRect = Rect.Left
            return True

        if self._rightControlRect.contains(pos):
            self._selectedCtrlRect = Rect.Right
            return True

        return False

    def itemChange(
        self, change: QGraphicsItem.GraphicsItemChange, value: typing.Any
    ) -> typing.Any:
        if change == QGraphicsItem.ItemPositionChange and self.scene():
            return QPointF(grid.Grid.alignTo(value.x()), self.pos().y())

        return super().itemChange(change, value)

    def changeItemWidth(self, pos: QPointF) -> None:
        delta = pos.x() - self._resizeOrigin
        if abs(delta) < grid.__width__:
            return

        r = QRectF(self._rect)
        self.prepareGeometryChange()

        if self._selectedCtrlRect == Rect.Left:
            if delta > 0:
                r.adjust(grid.__width__, 0, 0, 0)

                if r.width() >= grid.__width__:
                    self._rect = r
                    self._leftControlRect.adjust(grid.__width__, 0, grid.__width__, 0)
                    self.sigTrackDurationChanged.emit(self._rect.width())
            elif delta < 0:
                self._rect.adjust(-grid.__width__, 0, 0, 0)
                self._leftControlRect.adjust(-grid.__width__, 0, -grid.__width__, 0)
                self.sigTrackDurationChanged.emit(self._rect.width())

        elif self._selectedCtrlRect == Rect.Right:
            if delta > 0:
                self._rect.adjust(0, 0, grid.__width__, 0)
                self._rightControlRect.adjust(grid.__width__, 0, grid.__width__, 0)
                self.sigTrackDurationChanged.emit(self._rect.width())
            elif delta < 0:
                r.adjust(0, 0, -grid.__width__, 0)

                if r.width() >= grid.__width__:
                    self._rect = r
                    self._rightControlRect.adjust(
                        -grid.__width__, 0, -grid.__width__, 0
                    )
                    self.sigTrackDurationChanged.emit(self._rect.width())

        self._resizeOrigin = pos.x()

    def hoverMoveEvent(self, e: QGraphicsSceneHoverEvent) -> None:
        if self.isSelected():
            if self.insideControlRects(e.pos()):
                self.setCursor(Qt.SizeHorCursor)
            else:
                self.setCursor(Qt.ArrowCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

        super().hoverMoveEvent(e)

    def mousePressEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        if e.buttons() == Qt.LeftButton:
            if self.isSelected() and self.insideControlRects(e.pos()):
                self._isResizing = True
                self.setOpacity(0.3)
                self._resizeOrigin = e.pos().x()

        super().mousePressEvent(e)

    def mouseMoveEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        if self._isResizing:
            self.changeItemWidth(e.pos())
        else:
            super().mouseMoveEvent(e)

    def mouseReleaseEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        if self._isResizing:
            self._isResizing = False
            self.setOpacity(1)

        super().mouseReleaseEvent(e)

    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget
    ) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.black, 0, Qt.SolidLine)
        pen.setCosmetic(True)
        painter.setPen(pen)

        if self.isSelected():
            painter.setBrush(self.__selectedColor__)
        else:
            painter.setBrush(self.__normalColor__)

        painter.drawRect(self._rect)
