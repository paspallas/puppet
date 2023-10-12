from enum import Enum

from PyQt5.QtCore import (
    QAbstractItemModel,
    QEvent,
    QModelIndex,
    QObject,
    QPoint,
    QRect,
    QSize,
    Qt,
    QVariant,
)
from PyQt5.QtGui import QIcon, QKeyEvent, QMouseEvent, QPainter
from PyQt5.QtWidgets import QItemDelegate, QStyle, QStyleOptionViewItem

import src.app.resources.resources


class IconType(Enum):
    VisibleIcon = 1
    LockedIcon = 2


class IconCheckDelegate(QItemDelegate):
    def __init__(self, icon: IconType, exclusive: bool, parent: QObject):
        """Delegate for drawing an icon in SpriteListView for displaying
        visibility and locked state

            Args:
                icon (IconType): what icon we want to display
                exclusive (bool): whether we want to display only the icon or the normal display role
                parent (QObject): parent view
        """

        super().__init__(parent)

        self._checkedIcon: QIcon = None
        self._uncheckedIcon: QIcon = None
        self._exclusive: bool = exclusive

        if icon == IconType.VisibleIcon:
            self._checkedIcon = QIcon(":/icon/16/hidden.png")
            self._uncheckedIcon = QIcon(":/icon/16/visible.png")
        elif icon == IconType.LockedIcon:
            self._checkedIcon = QIcon(":/icon/16/lock.png")
            self._uncheckedIcon = QIcon(":/icon/16/unlock.png")

        self.setClipping(False)

    def editorEvent(
        self,
        event: QEvent,
        model: QAbstractItemModel,
        option: QStyleOptionViewItem,
        index: QModelIndex,
    ) -> bool:

        if not self._exclusive:
            return super().editorEvent(event, model, option, index)

        # The item in the model must be checkable
        flags = model.flags(index)

        if (
            not (flags & Qt.ItemIsUserCheckable)
            or not (option.state & QStyle.State_Enabled)
            or not (flags & Qt.ItemIsEnabled)
        ):
            return False

        # Check that the item has a checkstate
        variant = QVariant(index.data(Qt.CheckStateRole))
        if not variant.isValid():
            return False

        # Check the right event type
        if (
            event.type() == QEvent.MouseButtonRelease
            or event.type() == QEvent.MouseButtonDblClick
            or event.type() == QEvent.MouseButtonPress
        ):
            mouseEvent = QMouseEvent(event)
            if mouseEvent.button() != Qt.LeftButton:
                return False

            # Consume double click events inside the check rect
            if (
                event.type() == QEvent.MouseButtonPress
                or event.type() == QEvent.MouseButtonDblClick
            ):
                return True

        elif event.type() == QEvent.KeyPress:
            keyEvent = QKeyEvent(event)
            if keyEvent.key() != Qt.Key_Space and keyEvent.key() != Qt.Key_Select:
                return False

        else:
            return False

        state = Qt.CheckState(int(variant.value()))
        state = Qt.Unchecked if state == Qt.Checked else Qt.Checked
        return model.setData(index, state, Qt.CheckStateRole)

    def drawCheck(
        self,
        painter: QPainter,
        option: QStyleOptionViewItem,
        rect: QRect,
        state: Qt.CheckState,
    ):
        r = option.rect if self._exclusive else rect
        icon = self._checkedIcon if state == Qt.Checked else self._uncheckedIcon
        pixmap = icon.pixmap(r.size())

        layoutSize = pixmap.size() / pixmap.devicePixelRatio()
        targetRect = QRect(QPoint(0, 0), layoutSize)
        targetRect.moveCenter(r.center())

        painter.drawPixmap(targetRect, pixmap)

    def drawDisplay(
        self,
        painter: QPainter,
        option: QStyleOptionViewItem,
        rect: QRect,
        text: str,
    ):
        """Paints the normal widget display role"""

        if self._exclusive:
            return

        super().drawDisplay(painter, option, rect, text)

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        if self._exclusive:
            return QSize(32, 32)
        return super().sizeHint(option, index)
