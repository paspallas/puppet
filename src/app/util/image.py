from PyQt5.QtCore import QPoint, QRect, QSize, Qt
from PyQt5.QtGui import QColor, QPainter, QPixmap


class Image:
    @staticmethod
    def setAlpha(opacity: int, pixmap: QPixmap) -> QPixmap:
        transparent = QPixmap(pixmap.size())
        transparent.fill(Qt.transparent)

        painter = QPainter(transparent)
        painter.setOpacity(opacity * 0.01)
        painter.drawPixmap(QPoint(), pixmap)
        painter.end()

        return transparent

    @staticmethod
    def setTint(opacity: int, tint: QColor, pixmap: QPixmap) -> QPixmap:
        alpha_mask = Image.setAlpha(opacity, pixmap)
        tinted = QPixmap(alpha_mask)

        painter = QPainter(alpha_mask)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), tint)
        painter.end()

        painter.begin(tinted)
        painter.setCompositionMode(QPainter.CompositionMode_Overlay)
        painter.drawPixmap(QPoint(0, 0), alpha_mask, alpha_mask.rect())
        painter.end()

        return tinted

    @staticmethod
    def copyRegion(x: int, y: int, w: int, h: int, path: str) -> QPixmap:
        source = QPixmap(path)
        copy = QPixmap(w, h)

        painter = QPainter(copy)
        painter.drawPixmap(QPoint(0, 0), source, QRect(x, y, w, h))
        painter.end()

        return copy
