from PyQt5.QtCore import QObject, QPoint, Qt, pyqtSlot
from PyQt5.QtGui import QBrush, QColor, QKeyEvent, QPainter, QPixmap, QTransform
from PyQt5.QtWidgets import (
    QAction,
    QGraphicsItem,
    QGraphicsPixmapItem,
    QGraphicsSceneContextMenuEvent,
    QGraphicsSceneMouseEvent,
    QMenu,
    QWidget,
)

from .spritesheet import Frame, SpriteSheet
from ..util import Image

DEFAULT_ALPHA_MASK = "#FF00FF"


class Sprite(QGraphicsPixmapItem):
    def __init__(self, pixmap: QPixmap, x: int = 0, y: int = 0, parent: QWidget = None):
        super().__init__(parent=parent)

        self._pixmap: QPixmap = pixmap

        self.x = x
        self.y = y
        self._opacity = 100
        self._tint = None
        self._vertically_flipped = False
        self._horizontally_flipped = False

        self._setItemFlags()
        self.setAlphaMask()
        self.setPixmap(self._pixmap)

    @staticmethod
    def fromSpriteSheetFrame(frame: Frame, sheet_path: str):
        return Sprite(Image.copyRegion(*frame.rect(), sheet_path), *frame.topLeft())

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

    def setOpacity(self, opacity: float) -> QPixmap:
        self._opacity = opacity

        if self._tint is None:
            self.setPixmap(Image.setAlpha(opacity, self._pixmap))
        else:
            self.setPixmap(Image.setTint(opacity, self._tint, self._pixmap))

    def setTintColor(self, color: QColor) -> None:
        self._tint = color
        self.setPixmap(Image.setTint(self._opacity, color, self._pixmap))

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
        m33 = transform.m33()  # Additional Projection Factor

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
        m33 = transform.m33()  # Additional Projection Factor

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
        if e.key() == Qt.Key.Key_V:
            e.accept()
            self.flipVertical()
        elif e.key() == Qt.Key.Key_H:
            e.accept()
            self.flipHorizontal()
        else:
            super().keyPressEvent(e)

    # def contextMenuEvent(self, e: QGraphicsSceneContextMenuEvent):
    #     menu = QMenu()
    #     clone = menu.addAction("Clone", self.cloneAction)
    #     selected = menu.exec_(e.screenPos())

    # def cloneAction(self):
    #     clone = self.copy()
    #     self.scene().addItem(clone)


class SpriteGroup:
    """Collection of sprite items created from a spritesheet
    Represents a view of the sprites to be used in the editor
    """

    def __init__(self, sheet: SpriteSheet):
        self._collection: list[Sprite] = list()

        self._addSprites(sheet)

    def __iter__(self):
        self._currentIndex = 0
        return self

    def __next__(self):
        if self._currentIndex < len(self._collection):
            sprite = self._collection[self._currentIndex]
            self._currentIndex += 1
            return sprite
        raise StopIteration

    def _addSprites(self, sheet: SpriteSheet):
        for frame in sheet:
            sprite = Sprite.fromSpriteSheetFrame(frame, sheet.path)
            sprite.setPos(*frame.topLeft())
            sprite.lock()
            self._collection.append(sprite)

    def hide(self):
        for sprite in self._collection:
            sprite.hide()

    def show(self):
        for sprite in self._collection:
            sprite.show()


class SpriteObject(QObject):
    def __init__(self, parent: QObject = None):
        super().__init__(parent)

        self._spriteItem: Sprite = None

    def setSpriteItem(self, item: Sprite):
        print("new sprite item")
        self._spriteItem = item

    @pyqtSlot(int)
    def setOpacity(self, opacity: int) -> None:
        print(f"opacity val: {opacity}")
        self._spriteItem.setOpacity(opacity)
