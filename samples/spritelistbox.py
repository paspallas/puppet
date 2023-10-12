import sys
import pickle
import qtmodern.styles
from typing import Any

from PyQt5.QtCore import (
    QPoint,
    QRectF,
    QSize,
    QSizeF,
    Qt,
    pyqtSlot,
    QAbstractItemModel,
    QModelIndex,
    QVariant,
    QMimeData,
    QByteArray,
    QDataStream,
    QIODevice,
)
from PyQt5.QtGui import QColor, QPainter, QPaintEvent
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QAbstractItemView,
    QDataWidgetMapper,
)

from src.app.model.sprite import Sprite, SpriteObject
from src.app.util.reflection import PropertyList
from spritelistbox_ui import SpriteListBoxUi
from icondelegate import IconCheckDelegate, IconType


class SpriteListBox(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self._container = QWidget()
        self._ui = SpriteListBoxUi()
        self._ui.setupUi(self._container)
        self.setCentralWidget(self._container)

        # edit the three last fields with a data mapper
        self._mapper = QDataWidgetMapper(self)

    def setModel(self, model: QAbstractItemModel) -> None:
        self._model = model
        self._ui.list.setModel(self._model)

        self._mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self._mapper.setModel(self._model)
        self._mapper.addMapping(self._ui.opacitySlide, 3)
        self._mapper.addMapping(self._ui.flipHorizontalChk, 4)
        self._mapper.addMapping(self._ui.flipVerticalChk, 5)

        # delegate
        self._ui.list.setItemDelegateForColumn(
            7, IconCheckDelegate(IconType.VisibleIcon, True, self._ui.list)
        )
        self._ui.list.setItemDelegateForColumn(
            8, IconCheckDelegate(IconType.LockedIcon, True, self._ui.list)
        )

    def makeConnections(self) -> None:
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
        self._ui.list.selectionModel().currentRowChanged.connect(
            self._mapper.setCurrentModelIndex
        )

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


class KeyFrameData:
    def __init__(self, name: str, x: int, y: int, vflip: bool, hflip: bool, alpha: int):
        self._name: str = name
        self._x: int = x
        self._y: int = y
        self._vflip: bool = vflip
        self._hflip: bool = hflip
        self._transparency: int = alpha
        self._zIndex: int = 0
        self._hide: bool = False
        self._lock: bool = False

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int):
        self._x = value

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: int):
        self._y = value

    @property
    def alpha(self) -> int:
        return self._transparency

    @alpha.setter
    def alpha(self, value: int):
        self._transparency = value

    @property
    def hflip(self) -> bool:
        return self._hflip

    @hflip.setter
    def hflip(self, value: bool):
        self._hflip = value

    @property
    def vflip(self) -> bool:
        return self._vflip

    @vflip.setter
    def vflip(self, value: bool):
        self._vflip = value

    @property
    def zIndex(self) -> int:
        return self._zIndex

    @zIndex.setter
    def zIndex(self, value: int):
        self._zIndex = value

    @property
    def hide(self) -> bool:
        return self._hide

    @hide.setter
    def hide(self, value: bool):
        self._hide = value

    @property
    def lock(self) -> bool:
        return self._lock

    @lock.setter
    def lock(self, value: bool):
        self._lock = value

    def copy(self):
        item = KeyFrameData(
            self.name,
            self.x,
            self.y,
            self.vflip,
            self.hflip,
            self.alpha,
        )
        item.zIndex = self.zIndex
        item.hide = self.hide
        item.lock = self.lock
        item.name += "_copy"
        return item


class KeyFrames:
    def __init__(self):
        self._frames: list[KeyFrameData] = []
        self._property = PropertyList(KeyFrameData)

    def add(self, keyframe: KeyFrameData) -> None:
        keyframe.zIndex = len(self)
        self._frames.insert(0, keyframe)

    def copy(self, dst: int, src: int) -> None:
        item = self._frames[src]
        self._frames.insert(dst, item.copy())
        self.recalcZindexes()

    def get(self, item_index: int, attr_index: int) -> Any:
        return getattr(self._frames[item_index], self._property[attr_index])

    def set(self, item_index: int, attr_index: int, value: Any) -> None:
        setattr(self._frames[item_index], self._property[attr_index], value)

    def __len__(self) -> int:
        return len(self._frames)

    def count(self) -> int:
        return self._property.count()

    def moveup(self, item_index: int) -> None:
        item = self._frames.pop(item_index)
        self._frames.insert(item_index - 1, item)
        self.recalcZindexes()

    def movedown(self, item_index: int) -> None:
        item = self._frames.pop(item_index)
        self._frames.insert(item_index + 1, item)
        self.recalcZindexes()

    def moveTo(self, dst: int, src: int) -> None:
        item = self._frames.pop(src)
        self._frames.insert(dst, item)
        self.recalcZindexes()

    def deleteItem(self, item_index: int) -> None:
        self._frames.pop(item_index)
        self.recalcZindexes()

    def recalcZindexes(self) -> None:
        for i, item in enumerate(reversed(self._frames)):
            item.zIndex = i


class KeyFrameModel(QAbstractItemModel):
    def __init__(self, source: KeyFrames):
        super().__init__()

        self._data: KeyFrames = source

    def data(self, index: QModelIndex, role: int):
        if not index.isValid():
            return QVariant()

        if role in [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole]:
            return QVariant(self._data.get(index.row(), index.column()))

        if role == Qt.ItemDataRole.CheckStateRole and index.column() in [7, 8]:
            return QVariant(self._data.get(index.row(), index.column()))

        return QVariant()

    def setData(self, index: QModelIndex, value: Any, role: int) -> bool:
        if role == Qt.EditRole:
            self._data.set(index.row(), index.column(), value)
            self.dataChanged.emit(index, QModelIndex(), [])
            return True

        if role == Qt.CheckStateRole:
            self._data.set(index.row(), index.column(), value)
            self.dataChanged.emit(index, QModelIndex(), [])
            return True

        return False

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        self._headers = [
            "name",
            "x",
            "y",
            "alpha",
            "hflip",
            "vflip",
            "zindex",
            "hide",
            "lock",
        ]

        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Horizontal:
            return self._headers[section]

        return QVariant()

    def flags(self, index: QModelIndex):
        if not index.isValid():
            return Qt.NoItemFlags

        flags = (
            Qt.ItemIsEditable
            | Qt.ItemIsDropEnabled
            | Qt.ItemIsDragEnabled
            | Qt.ItemIsEditable
            | Qt.ItemIsEnabled
            | super().flags(index)
        )

        if index.column() in [7, 8]:
            return flags | Qt.ItemIsUserCheckable

        return flags

    def index(self, row: int, column: int, parent: QModelIndex) -> QModelIndex:
        if row < 0 or row >= len(self._data):
            return QModelIndex()
        return self.createIndex(row, column)

    def rowCount(self, parent: QModelIndex) -> int:
        if parent.isValid():
            return 0
        return len(self._data)

    def columnCount(self, parent: QModelIndex) -> int:
        return self._data.count()

    def parent(self, index: QModelIndex) -> QModelIndex:
        return QModelIndex()

    def moveRowUp(self, index: QModelIndex) -> bool:
        if index.row() == 0:
            return False

        self.layoutAboutToBeChanged.emit()
        self._data.moveup(index.row())
        self.layoutChanged.emit()
        return True

    def moveRowDown(self, index: QModelIndex) -> bool:
        if index.row() == len(self._data) - 1:
            return False

        self.layoutAboutToBeChanged.emit()
        self._data.movedown(index.row())
        self.layoutChanged.emit()
        return True

    def removeRow(self, row: int, parent: QModelIndex):
        self.beginRemoveRows(QModelIndex(), row, row)
        self._data.deleteItem(row)
        self.endRemoveRows()

    def mimeTypes(self) -> [str]:
        return ["application/puppet-framedata"]

    def mimeData(self, indexes: [QModelIndex]) -> QMimeData:
        encode = []
        encode.append(indexes[0].row())

        for index in indexes:
            if index.isValid():
                encode.append(self.data(index, Qt.ItemDataRole.DisplayRole).value())

        mimedata = QMimeData()
        mimedata.setData(self.mimeTypes()[0], bytearray(pickle.dumps(encode)))

        return mimedata

    def supportedDropActions(self) -> Qt.DropActions:
        return Qt.MoveAction | Qt.CopyAction

    def supportedDragActions(self) -> Qt.DropActions:
        return Qt.MoveAction | Qt.CopyAction

    def dropMimeData(
        self,
        data: QMimeData,
        action: Qt.DropAction,
        row: int,
        column: int,
        parent: QModelIndex,
    ) -> bool:

        if not self.canDropMimeData(data, action, row, column, parent):
            return False

        if action == Qt.IgnoreAction:
            return True

        decoded = []
        if data.hasFormat(self.mimeTypes()[0]):
            decoded = pickle.loads(data.data(self.mimeTypes()[0]).data())

            if action == Qt.MoveAction:
                self.layoutAboutToBeChanged.emit()
                self._data.moveTo(parent.row(), int(decoded[0]))
                self.layoutChanged.emit()

            elif action == Qt.CopyAction:
                self.layoutAboutToBeChanged.emit()
                self._data.copy(parent.row(), int(decoded[0]))
                self.layoutChanged.emit()

            return True

        return False


def main():
    frames = KeyFrames()
    frames.add(KeyFrameData("head_0", 1, 2, False, False, 50))
    frames.add(KeyFrameData("leg_1", 34, 23, True, False, 60))
    frames.add(KeyFrameData("chest_3", 10, 2, True, True, 20))
    frames.add(KeyFrameData("head_0", 1, 2, False, False, 50))
    frames.add(KeyFrameData("leg_4", 34, 23, True, False, 60))
    frames.add(KeyFrameData("chest_5", 10, 2, True, True, 20))
    model = KeyFrameModel(frames)

    app = QApplication([])
    qtmodern.styles.dark(app)

    w = SpriteListBox()
    w.setModel(model)
    w.makeConnections()
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
