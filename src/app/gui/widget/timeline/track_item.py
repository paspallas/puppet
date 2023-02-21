import typing

import grid
from PyQt5.QtCore import (
    QEasingCurve,
    QRectF,
    Qt,
    QVariantAnimation,
    pyqtSignal,
    pyqtSlot,
)
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import (
    QGraphicsItem,
    QGraphicsObject,
    QGraphicsRectItem,
    QStyleOptionGraphicsItem,
    QWidget,
)


class TrackItem(QGraphicsObject):
    def __init__(self) -> None:
        super().__init__()

        self._color: QColor = QColor(255, 255, 255, 150)
        self._animator = QVariantAnimation()
        self._animator.setDuration(160)
        self._connected = False

        flags = QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable
        self.setFlags(flags)

        self.setX(60)
        self.setY(60)

        self.rect1 = QGraphicsRectItem(self.x(), 80, 100, 20)
        self.rect1.setFlag(QGraphicsItem.ItemIsSelectable)
        self.rect1.setBrush(Qt.red)
        self.rect2 = QGraphicsRectItem(self.x(), 100, 120, 20)
        self.rect2.setBrush(Qt.green)

        self._collapsed = False
        self._children = [self.rect1, self.rect2]

    def addedToScene(self):
        self.scene().addItem(self.rect1)
        self.scene().addItem(self.rect2)

    def trackHeight(self) -> float:
        height = grid.__height__
        for child in self._children:
            height += child.rect().height()

        return height

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, 120, self.trackHeight())

    def mousePressEvent(self, e) -> None:
        if e.buttons() == Qt.LeftButton:
            if not self._collapsed:
                self.collapse()

        elif e.buttons() == Qt.RightButton:
            if self._collapsed:
                self.expand()

    def collapse(self) -> None:
        self.setupAnimator(grid.__height__, 0, self.animateCollapse)

    def expand(self) -> None:
        self.setupAnimator(0, grid.__height__, self.animateExpand)

    def animateCollapse(self, value: float) -> None:
        loop = self._animator.currentLoop()
        self.animate(value, len(self._children) - 1 - loop)

        if (
            value == 0
            and self._animator.currentLoop() == self._animator.loopCount() - 1
        ):
            self._collapsed = True

    def animateExpand(self, value: float) -> None:
        loop = self._animator.currentLoop()
        self.animate(value, loop)

        if value == grid.__height__:
            self._collapsed = False

    def animate(self, value: float, index: int) -> None:
        child = self._children[index]
        r = child.rect()
        r.setHeight(value)
        child.setRect(r)

        if value == 0:
            child.setVisible(False)
        elif value > 0 and not child.isVisible():
            child.setVisible(True)

    def setupAnimator(
        self, start: float, end: float, callback: typing.Callable
    ) -> None:
        self._animator.setStartValue(start)
        self._animator.setEndValue(end)
        self._animator.setLoopCount(2)

        if self._connected:
            self._animator.disconnect()

        self._animator.valueChanged.connect(callback)
        self._connected = True
        self._animator.start()

    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget
    ) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._color)
        painter.drawRect(self.boundingRect())
