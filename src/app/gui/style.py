from PyQt5.QtCore import QPoint, QRectF, QSize, QSizeF
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QWidget

__brushColor__ = QColor(66, 66, 66, 230)
__penColor__ = QColor(66, 66, 66, 255)
__boderRadius__ = 10
__inset__ = 0.5


def paintWidget(w: QWidget) -> None:
    with QPainter(w) as painter:
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(__penColor__)
        painter.setBrush(__brushColor__)
        rect = QRectF(
            QPoint(), QSizeF(w.size() - __inset__ * painter.pen().width() * QSize(1, 1))
        )
        painter.drawRoundedRect(rect, __boderRadius__, __boderRadius__)
