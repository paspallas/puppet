from PyQt5.QtCore import QPoint, QRect, QRectF, QSize, Qt
from PyQt5.QtGui import QColor, QImage, QPainter, QPixmap, QTransform
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsScene


class Image:
    __adjust__ = 0.5

    @staticmethod
    def setAlpha(alpha: int, pixmap: QPixmap) -> QPixmap:
        transparent = QPixmap(pixmap.size())
        transparent.fill(Qt.transparent)

        with QPainter(transparent) as painter:
            painter.setOpacity((100 - alpha) * 0.01)
            painter.drawPixmap(QPoint(), pixmap)

        return transparent

    @staticmethod
    def setTint(alpha: int, tint: QColor, pixmap: QPixmap) -> QPixmap:
        alpha_mask = Image.setAlpha(alpha, pixmap)
        tinted = QPixmap(alpha_mask)

        with QPainter(alpha_mask) as painter:
            painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
            painter.fillRect(pixmap.rect(), tint)

        with QPainter(tinted) as painter:
            painter.setCompositionMode(QPainter.CompositionMode_Overlay)
            painter.drawPixmap(QPoint(0, 0), alpha_mask, alpha_mask.rect())

        return tinted

    @staticmethod
    def flipHorizontal(item: QGraphicsItem) -> None:
        transform = item.transform()
        m11 = transform.m11()  # Horizontal scaling
        m12 = transform.m12()  # Vertical shearing
        m13 = transform.m13()  # Horizontal Projection
        m21 = transform.m21()  # Horizontal shearing
        m22 = transform.m22()  # vertical scaling
        m23 = transform.m23()  # Vertical Projection
        m31 = transform.m31()  # Horizontal Position (DX)
        m32 = transform.m32()  # Vertical Position (DY)
        m33 = transform.m33()  # Additional Projection Factor

        m31 = (
            0
            if m31 > 0
            else item.boundingRect()
            .adjusted(
                Image.__adjust__, Image.__adjust__, -Image.__adjust__, -Image.__adjust__
            )
            .width()
            * m11
        )

        transform.setMatrix(-m11, m12, m13, m21, m22, m23, m31, m32, m33)
        item.setTransform(transform)

    @staticmethod
    def flipVertical(item: QGraphicsItem) -> None:
        transform = item.transform()
        m11 = transform.m11()  # Horizontal scaling
        m12 = transform.m12()  # Vertical shearing
        m13 = transform.m13()  # Horizontal Projection
        m21 = transform.m21()  # Horizontal shearing
        m22 = transform.m22()  # vertical scaling
        m23 = transform.m23()  # Vertical Projection
        m31 = transform.m31()  # Horizontal Position (DX)
        m32 = transform.m32()  # Vertical Position (DY)
        m33 = transform.m33()  # Additional Projection Factor

        m32 = (
            0
            if m32 > 0
            else item.boundingRect()
            .adjusted(
                Image.__adjust__, Image.__adjust__, -Image.__adjust__, -Image.__adjust__
            )
            .height()
            * m22
        )

        transform.setMatrix(m11, m12, m13, m21, -m22, m23, m31, m32, m33)
        item.setTransform(transform)

    @staticmethod
    def thumbnailFromScene(scene: QGraphicsScene) -> QImage:
        scene.clearSelection()
        image = QImage(QSize(160, 112), QImage.Format_ARGB32)
        image.fill(Qt.transparent)

        with QPainter(image) as painter:
            painter.setRenderHint(QPainter.Antialiasing)
            scene.render(
                painter,
                QRectF(0, 0, 160, 112),
                scene.itemsBoundingRect(),
                Qt.KeepAspectRatio,
            )

        return image
