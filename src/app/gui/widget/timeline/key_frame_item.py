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

        self._rect = QRectF(x, y, w, h)

        flags = (
            QGraphicsItem.ItemIsSelectable
            | QGraphicsItem.ItemIsMovable
            | QGraphicsItem.ItemSendsGeometryChanges
            | QGraphicsItem.ItemSendsScenePositionChanges
        )

        self.setFlags(flags)
        self.setAcceptHoverEvents(True)

        self._leftControlRect = QRectF(
            x, y, self.__controlRectWidth__, self.__controlRectHeight__
        )
        self._rightControlRect = QRectF(
            (x + w) - self.__controlRectWidth__,
            y,
            self.__controlRectWidth__,
            self.__controlRectHeight__,
        )

        self._controlRect = None
        self._resizeOrigin = 0.0
        self._isResizing = False

    def boundingRect(self) -> QRectF:
        return self._rect

    def insideControlRects(self, pos: QPointF) -> bool:
        if self._leftControlRect.contains(pos):
            self._controlRect = Rect.Left
            return True

        if self._rightControlRect.contains(pos):
            self._controlRect = Rect.Right
            return True

        return False

    def itemChange(
        self, change: QGraphicsItem.GraphicsItemChange, value: typing.Any
    ) -> typing.Any:
        if change == QGraphicsItem.ItemPositionChange and self.scene():
            return QPointF(grid.alignToGrid(value.x()), self.pos().y())

        return super().itemChange(change, value)

    def changeItemWidth(self, pos: QPointF) -> None:
        self.prepareGeometryChange()

        delta = pos.x() - self._resizeOrigin
        if abs(delta) < grid.__width__:
            return

        r = QRectF(self._rect)

        if self._controlRect == Rect.Left:
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
        elif self._controlRect == Rect.Right:
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
        if self.insideControlRects(e.pos()):
            self.setCursor(Qt.SizeHorCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

        super().hoverMoveEvent(e)

    def mouseMoveEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        if self._isResizing:
            self.changeItemWidth(e.pos())

        else:
            super().mouseMoveEvent(e)

    def mousePressEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        if e.buttons() == Qt.LeftButton:
            if self.insideControlRects(e.pos()):
                self._isResizing = True
                self._resizeOrigin = e.pos().x()

        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        self._isResizing = False

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
