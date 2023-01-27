from PyQt5.QtCore import (
    QEvent,
    QLineF,
    QPoint,
    QPointF,
    QRectF,
    QSize,
    Qt,
    pyqtSignal,
    pyqtSlot,
)
from PyQt5.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QLinearGradient,
    QMouseEvent,
    QPainter,
    QPaintEvent,
    QPen,
    QPixmap,
    QResizeEvent,
    QTransform,
)
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QSlider, QWidget


class ColorPickerWidget(QWidget):

    sigSelectedColorChanged = pyqtSignal(str)

    radius = 175
    size = radius / 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMouseTracking(True)
        self.setMinimumSize(QSize(200, 200))

        self.center = QPointF(self.width() / 2, self.height() / 2)
        self.hueRect = QRectF(0, 0, self.radius, self.radius)
        self.hueRect.moveCenter(self.rect().center())
        self.svRect = QRectF(0, 0, self.radius - 75, self.radius - 75)
        self.svRect.moveCenter(self.rect().center())

        self.selected_color = QColor(Qt.red)
        self.h = self.selected_color.hueF()
        self.s = self.selected_color.saturationF()
        self.v = self.selected_color.valueF()

        # mouse coords
        self.x = 0
        self.y = 0
        self.hueX = 0
        self.hueY = 0

        self.selRect = QRectF(20, 260, 100, 20)

        self.mapSatValToCartesianCoords()
        self.createGradients()

    def createGradients(self) -> None:
        self.hueGradient = QConicalGradient(self.center, 0)
        maxSteps = 11
        color = QColor()
        for step in reversed(range(maxSteps)):
            hue = step * 36
            color.setHsv(hue, 255, 255, 255)
            self.hueGradient.setColorAt(0.1 * step, color)

        self.satGradient = QLinearGradient(
            self.svRect.left(),
            self.svRect.bottom(),
            self.svRect.right(),
            self.svRect.bottom(),
        )

        self.valGradient = QLinearGradient(
            self.svRect.left(),
            self.svRect.bottom(),
            self.svRect.left(),
            self.svRect.top(),
        )

        self.updateSatValGradient()

    def updateSatValGradient(self):
        self.satGradient.setColorAt(
            0.0, QColor.fromHsv(self.selected_color.hue(), 0, 255, 255)
        )
        self.satGradient.setColorAt(
            1.0, QColor.fromHsv(self.selected_color.hue(), 255, 255, 255)
        )
        self.valGradient.setColorAt(0.0, QColor.fromRgb(0, 0, 0, 255))
        self.valGradient.setColorAt(1.0, QColor.fromRgb(0, 0, 0, 0))

    def mapSatValToCartesianCoords(self) -> None:
        lengthX = self.svRect.width() + self.svRect.left()
        lenghtY = self.svRect.height() + self.svRect.top()
        self.x = self.s * lengthX
        self.y = self.v * lenghtY - self.svRect.height()

    def mapCartesianCoordsToSatVal(self) -> None:
        self.s = (self.x - self.svRect.left()) / self.svRect.width()
        self.v = 1 - ((self.y - self.svRect.top()) / self.svRect.height())

    def mapCartesianCoordsToHue(self) -> None:
        line = QLineF(QPointF(self.rect().center()), QPointF(self.hueX, self.hueY))
        self.h = line.angle() / 360 % 1.0

    def recalc(self) -> None:
        self.selected_color.setHsvF(self.h, self.s, self.v)
        self.sigSelectedColorChanged.emit(self.selected_color.name())

        self.repaint()

    def isInsidePath(self, point: QPointF) -> bool:
        vector = QLineF(self.center, point)
        if self.size - 13 <= vector.length() <= self.size + 13:
            return True
        return False

    def processMouseEvent(self, e: QMouseEvent) -> None:
        hit = False
        x = y = 0

        if self.svRect.adjusted(-6, -6, 6, 6).contains(e.x(), e.y()):
            hit = True

            r = self.svRect
            if e.x() < r.left():
                x = r.left()
            elif e.x() > r.right():
                x = r.right()
            else:
                x = e.x()

            if e.y() < r.top():
                y = r.top()
            elif e.y() > r.bottom():
                y = r.bottom()
            else:
                y = e.y()

            if e.buttons() & Qt.LeftButton:
                self.x, self.y = x, y
                self.mapCartesianCoordsToSatVal()

        if self.isInsidePath(QPointF(e.x(), e.y())):
            hit = True

            if e.buttons() & Qt.LeftButton:
                self.hueX = e.x()
                self.hueY = e.y()
                self.mapCartesianCoordsToHue()
                self.selected_color.setHsvF(self.h, self.s, self.v)
                self.updateSatValGradient()

        if hit:
            if e.buttons() & Qt.LeftButton:
                self.recalc()
        else:
            self.setCursor(Qt.ArrowCursor)

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        self.processMouseEvent(e)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        self.processMouseEvent(e)

    def paintEvent(self, e: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        pen = QPen(QBrush(self.hueGradient), 12, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawArc(self.hueRect, 0, 360 * 16)

        pen.setBrush(Qt.black)
        pen.setWidth(0)
        painter.setPen(pen)
        painter.setBrush(self.satGradient)
        painter.drawRect(self.svRect)
        painter.setBrush(self.valGradient)
        painter.drawRect(self.svRect)
        painter.setBrush(self.selected_color)
        painter.drawRect(self.selRect)

        # hue
        line = QLineF.fromPolar(self.radius / 2, 360 * self.h)
        line.translate(self.rect().center())
        self.drawSelectionCursor(painter, pen, line.p2())

        # saturation, value
        self.drawSelectionCursor(painter, pen, QPointF(self.x, self.y), clip=True)

    def drawSelectionCursor(
        self, painter: QPainter, pen: QPen, point: QPointF, clip: bool = False
    ) -> None:
        if clip:
            painter.setClipRect(self.svRect)
        else:
            painter.setClipping(False)

        painter.setBrush(Qt.transparent)
        pen.setWidth(2)
        pen.setBrush(Qt.black)
        painter.setPen(pen)
        painter.drawEllipse(point, 4, 4)
        pen.setBrush(Qt.white)
        painter.setPen(pen)
        painter.drawEllipse(point, 6, 6)
