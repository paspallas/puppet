from PyQt5.QtCore import QPoint, QRect, Qt
from PyQt5.QtGui import QBrush, QColor, QKeyEvent, QPainter, QPixmap, QTransform
from PyQt5.QtWidgets import (
    QGraphicsItem,
    QGraphicsPixmapItem,
    QWidget,
    QGraphicsSceneMouseEvent,
)

DEFAULT_ALPHA_MASK = "#FF00FF"


class Sprite(QGraphicsPixmapItem):
    def __init__(self, pixmap: QPixmap, x: int = 0, y: int = 0, parent: QWidget = None):
        super().__init__(parent=parent)

        self._pixmap = pixmap

        self.x = x
        self.y = y
        self._opacity = 100
        self._tint = None
        self._vertically_flipped = False
        self._horizontally_flipped = False

        self._setItemFlags()
        self.setAlphaMask()
        self.setPixmap(self._pixmap)

    @classmethod
    def fromSpriteSheet(cls, x: int, y: int, w: int, h: int, sprite_sheet: QPixmap):
        pixmap = QPixmap(w, h)
        painter = QPainter(pixmap)
        painter.drawPixmap(QPoint(0, 0), sprite_sheet, QRect(x, y, w, h))
        painter.end()

        return cls(pixmap, x, y)

    def copy(self):
        clone = Sprite(self._pixmap, self.x, self.y)
        clone.setOpacity(self._opacity)

        if self._tint is not None:
            clone.setTintColor(self._tint)

        if self._vertically_flipped:
            clone.flipVertical()

        if self._horizontally_flipped:
            clone.flipHorizontal()

        return clone

    __copy__ = copy

    def _setItemFlags(self):
        flags = (
            QGraphicsItem.ItemIsSelectable
            | QGraphicsItem.ItemIsMovable
            | QGraphicsItem.ItemIsFocusable
            | QGraphicsItem.ItemSendsScenePositionChanges
        )

        self.setFlags(flags)
        self.setAcceptHoverEvents(True)

    def setAlphaMask(self):
        self._pixmap.setMask(
            self._pixmap.createMaskFromColor(QColor(DEFAULT_ALPHA_MASK))
        )

    def setOpacity(self, opacity: float) -> None:
        if 0 <= opacity <= 100.0:
            transparent = QPixmap(self._pixmap.size())
            transparent.fill(Qt.transparent)

            painter = QPainter(transparent)
            painter.setOpacity(opacity * 0.01)
            painter.drawPixmap(QPoint(), self._pixmap)
            painter.end()

            self._pixmap = transparent
            self.setPixmap(self._pixmap)
            self._opacity = opacity

    def setTintColor(self, color: QColor) -> None:
        painter = QPainter(self._pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceAtop)
        painter.fillRect(self._pixmap.rect(), color)
        painter.end()

        self.setPixmap(self._pixmap)
        self._tint = color

    def flipHorizontal(self) -> None:
        """Flip the sprite in the X axis"""
        self._horizontally_flipped = not self._horizontally_flipped

        transform = self.transform()
        m11 = transform.m11()  # Horizontal scaling
        m12 = transform.m12()  # Vertical shearing
        m13 = transform.m13()  # Horizontal Projection
        m21 = transform.m21()  # Horizontal shearing
        m22 = transform.m22()  # vertical scaling
        m23 = transform.m23()  # Vertical Projection
        m31 = transform.m31()  # Horizontal Position (DX)
        m32 = transform.m32()  # Vertical Position (DY)
        m33 = transform.m33()  # Addtional Projection Factor

        m31 = 0 if m31 > 0 else self.boundingRect().width() * m11

        transform.setMatrix(-m11, m12, m13, m21, m22, m23, m31, m32, m33)
        self.setTransform(transform)

    def flipVertical(self) -> None:
        """Flip the sprite in the Y axis"""
        self._vertically_flipped = not self._vertically_flipped

        transform = self.transform()
        m11 = transform.m11()  # Horizontal scaling
        m12 = transform.m12()  # Vertical shearing
        m13 = transform.m13()  # Horizontal Projection
        m21 = transform.m21()  # Horizontal shearing
        m22 = transform.m22()  # vertical scaling
        m23 = transform.m23()  # Vertical Projection
        m31 = transform.m31()  # Horizontal Position (DX)
        m32 = transform.m32()  # Vertical Position (DY)
        m33 = transform.m33()  # Addtional Projection Factor

        m32 = 0 if m32 > 0 else self.boundingRect().height() * m22

        transform.setMatrix(m11, m12, m13, m21, -m22, m23, m31, m32, m33)
        self.setTransform(transform)

    def lock(self) -> None:
        """Lock sprite movement"""
        self.setFlag(QGraphicsItem.ItemIsMovable, False)

    def unlock(self) -> None:
        """Unlock sprite movement"""
        self.setFlag(QGraphicsItem.ItemIsMovable, True)

    def keyPressEvent(self, e: QKeyEvent):
        super().keyPressEvent(e)

        if e.key() == Qt.Key.Key_V:
            self.flipVertical()
        elif e.key() == Qt.Key.Key_H:
            self.flipHorizontal()


class SpriteGroup:
    """Collection of sprites from a spritesheet"""

    def __init__(self):
        self._collection = []

    def add(self, sprite: Sprite):
        self._collection.append(sprite)

    def hide(self):
        for sprite in self._collection:
            sprite.hide()

    def show(self):
        for sprite in self._collection:
            sprite.show()
