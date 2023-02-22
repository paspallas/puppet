import typing
from enum import IntEnum

import grid
from PyQt5.QtCore import QPointF, QRectF, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QFontMetrics, QPainter, QPen
from PyQt5.QtWidgets import (
    QGraphicsItem,
    QGraphicsObject,
    QGraphicsSceneHoverEvent,
    QGraphicsSceneMouseEvent,
    QStyleOptionGraphicsItem,
    QWidget,
)


class Handle(IntEnum):
    Left = 0
    Right = 1


class State(IntEnum):
    Iddle = 0
    Resize = 1


class KeyFrameItem(QGraphicsObject):
    __selectedColor__ = QColor(Qt.cyan)
    __normalColor__ = QColor(Qt.magenta)
    __handleWidth__ = 2
    __handleHeight__ = grid.__height__

    keyDurationChange = pyqtSignal(float)

    def __init__(self, x: float, y: float, w: float, h: float) -> None:
        super().__init__()
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

        self._rect = QRectF(0, 0, w, h)
        self.setX(x)
        self.setY(y)

        self._leftHandle = QRectF(0, 0, self.__handleWidth__, self.__handleHeight__)
        self._rightHandle = QRectF(
            w - self.__handleWidth__,
            0,
            self.__handleWidth__,
            self.__handleHeight__,
        )

        self._states: typing.Dict[State, typing.Callable] = {
            State.Iddle: self._paintIddle,
            State.Resize: self._paintResize,
        }
        self._state = State.Iddle
        self._selectedHandle = None
        self._resizeOrigin = 0.0

    def boundingRect(self) -> QRectF:
        return self._rect

    def isInsideHandle(self, localPos: QPointF) -> bool:
        if self._leftHandle.contains(localPos):
            self._selectedHandle = Handle.Left
            return True

        if self._rightHandle.contains(localPos):
            self._selectedHandle = Handle.Right
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

        if self._selectedHandle == Handle.Left:
            if delta > 0:
                r.adjust(grid.__width__, 0, 0, 0)

                if r.width() >= grid.__width__:
                    self._rect = r
                    self._leftHandle.adjust(grid.__width__, 0, grid.__width__, 0)
                    self.keyDurationChange.emit(self._rect.width())
            elif delta < 0:
                self._rect.adjust(-grid.__width__, 0, 0, 0)
                self._leftHandle.adjust(-grid.__width__, 0, -grid.__width__, 0)
                self.keyDurationChange.emit(self._rect.width())

        elif self._selectedHandle == Handle.Right:
            if delta > 0:
                self._rect.adjust(0, 0, grid.__width__, 0)
                self._rightHandle.adjust(grid.__width__, 0, grid.__width__, 0)
                self.keyDurationChange.emit(self._rect.width())
            elif delta < 0:
                r.adjust(0, 0, -grid.__width__, 0)

                if r.width() >= grid.__width__:
                    self._rect = r
                    self._rightHandle.adjust(-grid.__width__, 0, -grid.__width__, 0)
                    self.keyDurationChange.emit(self._rect.width())

        self._resizeOrigin = pos.x()

    def start(self) -> int:
        return int(self.x() + self._rect.x()) // grid.__width__

    def end(self) -> int:
        return int(self.x() + self._rect.x() + self._rect.width()) // grid.__width__

    def hoverMoveEvent(self, e: QGraphicsSceneHoverEvent) -> None:
        if self.isSelected():
            if self.isInsideHandle(e.pos()):
                self.setCursor(Qt.SizeHorCursor)
            else:
                self.setCursor(Qt.ArrowCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

        super().hoverMoveEvent(e)

    def mousePressEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        if e.buttons() == Qt.LeftButton:
            if self.isSelected():
                if self.isInsideHandle(e.pos()):
                    self._state = State.Resize
                    self._resizeOrigin = e.scenePos().x()

        super().mousePressEvent(e)

    def mouseMoveEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        if self._state == State.Resize:
            self.changeItemWidth(e.scenePos())
        else:
            super().mouseMoveEvent(e)

    def mouseReleaseEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        if self._state == State.Resize:
            self._state = State.Iddle

        super().mouseReleaseEvent(e)

    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget
    ) -> None:
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        pen = QPen(Qt.black, 0, Qt.SolidLine)
        pen.setCosmetic(True)
        painter.setPen(pen)

        func = self._states.get(self._state, self._paintIddle)
        return func(painter, pen)

    def _paintIddle(self, painter: QPainter, pen: QPen) -> None:
        if self.isSelected():
            painter.setBrush(self.__selectedColor__)
        else:
            painter.setBrush(self.__normalColor__)
        painter.drawRect(self._rect)

    def _paintResize(self, painter: QPainter, pen: QPen) -> None:
        painter.setBrush(self.__selectedColor__)
        painter.save()
        painter.setOpacity(0.3)
        painter.drawRect(self._rect)
        painter.restore()
        pen.setColor(Qt.white)
        painter.setPen(pen)

        label = f"{int(self._rect.width() // grid.__width__)}f"
        fm = self.scene().views()[0].viewport().fontMetrics()
        r = QRectF(
            fm.boundingRect(label).translated(
                int(self._rect.width() // 2 + self._rect.x()), 0
            )
        )
        r.translate(-r.width() / 2, r.height())
        painter.drawText(r, label)
