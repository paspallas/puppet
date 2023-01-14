from PyQt5.QtCore import QPoint, QRect, QSize, Qt
from PyQt5.QtGui import QColor, QPainter, QPixmap


class Image:
    @staticmethod
    def setAlpha(opacity: int, pixmap: QPixmap) -> QPixmap:
        transparent = QPixmap(pixmap.size())
        transparent.fill(Qt.transparent)

        with QPainter(transparent) as painter:
            painter.setOpacity(opacity * 0.01)
            painter.drawPixmap(QPoint(), pixmap)

        return transparent

    @staticmethod
    def setTint(opacity: int, tint: QColor, pixmap: QPixmap) -> QPixmap:
        alpha_mask = Image.setAlpha(opacity, pixmap)
        tinted = QPixmap(alpha_mask)

        with QPainter(alpha_mask) as painter:
            painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
            painter.fillRect(pixmap.rect(), tint)

        with QPainter(tinted) as painter:
            painter.setCompositionMode(QPainter.CompositionMode_Overlay)
            painter.drawPixmap(QPoint(0, 0), alpha_mask, alpha_mask.rect())

        return tinted
