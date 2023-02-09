from PyQt5.QtCore import (
    QLineF,
    QPoint,
    QRectF,
    QSize,
    Qt,
    pyqtProperty,
    pyqtSignal,
    pyqtSlot,
)
from PyQt5.QtGui import (
    QColor,
    QFontMetrics,
    QMouseEvent,
    QPainter,
    QPainterPath,
    QPaintEvent,
    QPen,
    QResizeEvent,
)
from PyQt5.QtWidgets import QWidget, qApp


class Ruler(QWidget):
    sizeChanged = pyqtSignal(QSize)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._offset = 1.0
        self.setFixedHeight(20)
        self.move(0, 0)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.translate(0, -self._offset)
        widthMM = int(self.width() * self.toMM())
        painter.setFont(self.font())
        fm = QFontMetrics(self.font())

        for position in range(0, widthMM):
            positionInPix = int(position / self.toMM())
            if position % 10 == 0:
                if position != 0:
                    txt = str(position)
                    txtRect = QRectF(fm.boundingRect(txt).translated(positionInPix, 0))
                    txtRect.translate(txtRect.width() // 2, 0)
                    painter.drawText(txtRect, txt)

                painter.drawLine(positionInPix, 5, positionInPix, 15)

            else:
                painter.drawLine(positionInPix, 5, positionInPix, 10)

    def resizeEvent(self, event: QResizeEvent) -> None:
        maximumMM = event.size().width() * self.toMM()
        fm = QFontMetrics(self.font())
        w = fm.width(str(maximumMM)) + 20

        if w != event.size().width():
            newSize = QSize(event.size().width(), 20)
            self.sizeChanged.emit(newSize)
            return self.setFixedSize(newSize)

        return super().resizeEvent(event)

    @pyqtSlot(int)
    def setOffset(self, value: int) -> None:
        self._offset = value
        self.update()

    def toMM(self) -> float:
        return 25.4 / qApp.desktop().logicalDpiX()
