from PyQt5.QtCore import (
    QAbstractItemModel,
    QObject,
    QModelIndex,
    Qt,
    QRectF,
    QPoint,
    QSizeF,
    QSize,
    QVariant,
    pyqtSlot,
)
from PyQt5.QtGui import QPainter, QPaintEvent
from PyQt5.QtWidgets import QAbstractItemView, QDataWidgetMapper, QGraphicsItem, QWidget

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
        self._ui.updateHeaders()
        self._mapper.setModel(model)

        # connect to the datamapper after the model has been set
        self._ui.list.selectionModel().currentRowChanged.connect(
            self._mapper.setCurrentModelIndex
        )
        self._ui.list.setItemDelegateForColumn(
            1, IconCheckDelegate(IconType.VisibleIcon, True, self._ui.list)
        )

        self._delegate = IconCheckDelegate(IconType.LockedIcon, True, self._ui.list)
        self._ui.list.setItemDelegateForColumn(2, self._delegate)

        self._delegate.sigCheckState.connect(lambda val: self._ui.xSpin.setEnabled(val))
        self._delegate.sigCheckState.connect(lambda val: self._ui.ySpin.setEnabled(val))
        self._delegate.sigCheckState.connect(
            lambda val: self._ui.opacitySlide.setEnabled(val)
        )
        self._delegate.sigCheckState.connect(
            lambda val: self._ui.flipHorizontalChk.setEnabled(val)
        )
        self._delegate.sigCheckState.connect(
            lambda val: self._ui.flipVerticalChk.setEnabled(val)
        )

        self._mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self._mapper.addMapping(self._ui.xSpin, 3)
        self._mapper.addMapping(self._ui.ySpin, 4)
        self._mapper.addMapping(self._ui.opacitySlide, 5)
        self._mapper.addMapping(self._ui.flipHorizontalChk, 6)
        self._mapper.addMapping(self._ui.flipVerticalChk, 7)

    def _makeConnections(self) -> None:
        self._ui.upBtn.clicked.connect(self._moveItemUp)
        self._ui.downBtn.clicked.connect(self._moveItemDown)
        self._ui.delBtn.clicked.connect(self._deleteItem)

        # Changes in the datamapper must be reflected inmediately in the model
        self._ui.xSpin.valueChanged.connect(self._mapper.submit, Qt.QueuedConnection)
        self._ui.ySpin.valueChanged.connect(self._mapper.submit, Qt.QueuedConnection)
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

    @pyqtSlot(int)
    def updateDataMapper(self, index: int) -> None:
        """Trigger the mapper to update when the data source of the model changes"""

        self._mapper.setCurrentIndex(index)

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

    @pyqtSlot(QGraphicsItem)
    def setCurrentItem(self, item: QGraphicsItem) -> None:
        """Set the current item when the users selects an item in the editor view"""

        self._ui.list.setCurrentIndex(
            self._ui.list.model().itemFromZValue(int(item.zValue()))
        )

    def paintEvent(self, e: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(self._ui.penColor)
        painter.setBrush(self._ui.brushColor)
        rect = QRectF(
            QPoint(), QSizeF(self.size() - 0.5 * painter.pen().width() * QSize(1, 1))
        )
        painter.drawRoundedRect(rect, 2, 2)
