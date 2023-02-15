from PyQt5.QtCore import (
    QAbstractItemModel,
    QModelIndex,
    QObject,
    Qt,
    QVariant,
    pyqtSignal,
    pyqtSlot,
)
from PyQt5.QtGui import QPaintEvent
from PyQt5.QtWidgets import QAbstractItemView, QGraphicsItem, QWidget

from ..delegate.icon_delegate import IconCheckDelegate, IconType
from .. import style
from .sprite_list_box_ui import SpriteListBoxUi


class SpriteListBox(QWidget):
    sigEnabledChanged = pyqtSignal(bool)
    sigItemChanged = pyqtSignal(QModelIndex)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self._ui = SpriteListBoxUi()
        self._ui.setupUi(self)
        self._makeConnections()

    def setModel(self, model: QAbstractItemModel) -> None:
        self._model = model
        self._model.sigModelRowCountChanged.connect(self.onListSizeChanged)

        self._ui.list.setModel(self._model)
        self._ui.updateHeaders()

        self._ui.list.setItemDelegateForColumn(
            1, IconCheckDelegate(IconType.VisibleIcon, True, self._ui.list)
        )

        self._lock = IconCheckDelegate(IconType.LockedIcon, True, self._ui.list)
        self._ui.list.setItemDelegateForColumn(2, self._lock)
        self._lock.sigCheckState.connect(self.sigEnabledChanged)

    def _makeConnections(self) -> None:
        self._ui.upBtn.clicked.connect(self._moveItemUp)
        self._ui.downBtn.clicked.connect(self._moveItemDown)
        self._ui.delBtn.clicked.connect(self._deleteItem)
        self._ui.copyBtn.clicked.connect(self._copyItem)
        self._ui.list.clicked.connect(self._selectItem)

    @pyqtSlot()
    def _moveItemUp(self) -> None:
        index = self._ui.list.currentIndex()
        if self._ui.list.model().moveRowUp(index):
            next_ = self._ui.list.model().createIndex(index.row() - 1, 0)
            self._ui.list.setCurrentIndex(next_)

    @pyqtSlot()
    def _moveItemDown(self) -> None:
        index = self._ui.list.currentIndex()
        if self._ui.list.model().moveRowDown(index):
            next_ = self._ui.list.model().createIndex(index.row() + 1, 0)
            self._ui.list.setCurrentIndex(next_)

    @pyqtSlot()
    def _deleteItem(self) -> None:
        index = self._ui.list.currentIndex()
        self._ui.list.model().removeRow(index.row(), QModelIndex())

    @pyqtSlot()
    def _copyItem(self) -> None:
        index = self._ui.list.currentIndex()
        self._ui.list.model().copyRow(index)

    @pyqtSlot(QModelIndex)
    def _selectItem(self, index: QModelIndex) -> None:
        self._ui.list.model().selectRow(index)
        self.sigItemChanged.emit(index)

    @pyqtSlot(int)
    def setCurrentItem(self, row: int) -> None:
        self._ui.list.setCurrentIndex(
            self._ui.list.model().createIndex(row, 0, QModelIndex())
        )

    @pyqtSlot(int)
    def onListSizeChanged(self, size: int) -> None:
        print("list size changed")
        if size > 0:
            self._buttonState(True)
        else:
            self._buttonState(False)

    def paintEvent(self, e: QPaintEvent):
        style.paintWidget(self)

    def _buttonState(self, enabled: bool) -> None:
        self._ui.upBtn.setEnabled(enabled)
        self._ui.downBtn.setEnabled(enabled)
        self._ui.copyBtn.setEnabled(enabled)
        self._ui.delBtn.setEnabled(enabled)
