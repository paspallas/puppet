from PyQt5.QtCore import (
    QAbstractItemModel,
    QModelIndex,
    Qt,
    QRectF,
    QPoint,
    QSizeF,
    QSize,
    QVariant,
    pyqtSlot,
)
from PyQt5.QtGui import QColor, QPainter, QPaintEvent
from PyQt5.QtWidgets import QAbstractItemView, QDataWidgetMapper, QWidget

from ...model.sprite import Sprite, SpriteObject
from ..delegate.icon_delegate import IconCheckDelegate, IconType
from .spritelistbox_ui import SpriteListBoxUi


class SpriteListBox(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self._mapper = QDataWidgetMapper(self)

        self._ui = SpriteListBoxUi()
        self._ui.setupUi(self)
        self._makeConnections()

    def setModel(self, model: QAbstractItemModel) -> None:
        self._ui.list.setModel(model)
        self._mapper.setModel(model)

        # connect to the mapper after the model has been set
        self._ui.list.selectionModel().currentRowChanged.connect(
            self._mapper.setCurrentModelIndex
        )
        self._ui.list.setItemDelegateForColumn(
            7, IconCheckDelegate(IconType.VisibleIcon, True, self._ui.list)
        )
        self._ui.list.setItemDelegateForColumn(
            8, IconCheckDelegate(IconType.LockedIcon, True, self._ui.list)
        )

        self._mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self._mapper.addMapping(self._ui.opacitySlide, 3)
        self._mapper.addMapping(self._ui.flipHorizontalChk, 4)
        self._mapper.addMapping(self._ui.flipVerticalChk, 5)

    def _makeConnections(self) -> None:
        self._ui.upBtn.clicked.connect(self._moveItemUp)
        self._ui.downBtn.clicked.connect(self._moveItemDown)
        self._ui.delBtn.clicked.connect(self._deleteItem)

        # realtime changes to the model from the mapper two ways
        self._ui.opacitySlide.valueChanged.connect(
            self._mapper.submit, Qt.QueuedConnection
        )
        self._ui.flipHorizontalChk.stateChanged.connect(
            self._mapper.submit, Qt.QueuedConnection
        )
        self._ui.flipVerticalChk.stateChanged.connect(
            self._mapper.submit, Qt.QueuedConnection
        )
        self._ui.list.clicked.connect(self.itemPressed)

    @pyqtSlot(QModelIndex)
    def itemPressed(self, index: QModelIndex):
        pass
        # print(
        #     self._model.index(index.row(), index.column(), QModelIndex).data(
        #         Qt.ItemDataRole.DisplayRole
        #     )
        # )

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

    def paintEvent(self, e: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QColor("#424242"))
        painter.setBrush(QColor("#353535"))
        rect = QRectF(
            QPoint(), QSizeF(self.size() - 0.5 * painter.pen().width() * QSize(1, 1))
        )
        painter.drawRoundedRect(rect, 4, 4)
