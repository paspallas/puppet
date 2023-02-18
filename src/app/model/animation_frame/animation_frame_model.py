import pickle
import typing

from PyQt5.QtCore import (
    QAbstractItemModel,
    QMimeData,
    QModelIndex,
    Qt,
    QVariant,
    pyqtSignal,
    pyqtSlot,
)

from .animation_frame import AnimationFrame
from .frame_sprite import Index


class AnimationFrameModel(QAbstractItemModel):
    """Interface between the view and the current editable animation frame"""

    def __init__(self):
        super().__init__()

        self._dataSource: AnimationFrame = None

    def setDataSource(self, source: AnimationFrame) -> None:
        self.beginResetModel()

        if self._dataSource is not None:
            self._dataSource.sigFrameDataChanged.disconnect()
            self._dataSource.sigFrameLayoutChanged.disconnect()

        self._dataSource = source
        self._dataSource.sigAddedItem.connect(self.newRow)
        self._dataSource.sigFrameDataChanged.connect(self.dataSourceChanged)
        self._dataSource.sigFrameLayoutAboutToChange.connect(
            lambda: self.layoutAboutToBeChanged.emit()
        )
        self._dataSource.sigFrameLayoutChanged.connect(
            lambda: self.layoutChanged.emit()
        )

        self.endResetModel()

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if not index.isValid():
            return QVariant()

        if role in [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole]:
            return QVariant(self._dataSource.get(index.row(), index.column()))

        if role == Qt.ItemDataRole.CheckStateRole and index.column() in [
            Index.Hide,
            Index.Lock,
        ]:
            return QVariant(self._dataSource.get(index.row(), index.column()))

        return QVariant()

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        if role == Qt.EditRole:
            self._dataSource.set(index.row(), index.column(), value)
            self.dataChanged.emit(index, QModelIndex(), [])
            return True

        if role == Qt.CheckStateRole:
            self._dataSource.set(index.row(), index.column(), value)
            self.dataChanged.emit(index, QModelIndex(), [])
            return True

        return False

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
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

        if index.column() in [Index.Hide, Index.Lock]:
            return flags | Qt.ItemIsUserCheckable

        return flags

    def index(self, row: int, column: int, parent: QModelIndex = ...) -> QModelIndex:
        if row < 0 or row >= len(self._dataSource):
            return QModelIndex()
        return self.createIndex(row, column)

    def rowCount(self, parent: QModelIndex = ...) -> int:
        if parent.isValid():
            return 0
        return len(self._dataSource)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 3

    def parent(self, child: QModelIndex) -> QModelIndex:
        return QModelIndex()

    def newRow(self) -> None:
        self.beginInsertRows(QModelIndex(), 0, 0)
        self.endInsertRows()

    def moveRowUp(self, index: QModelIndex) -> bool:
        if index.row() == 0:
            return False

        self.layoutAboutToBeChanged.emit()
        self._dataSource.moveUp(index.row())
        self.layoutChanged.emit()

        return True

    def moveRowDown(self, index: QModelIndex) -> bool:
        if index.row() == len(self._dataSource) - 1:
            return False

        self.layoutAboutToBeChanged.emit()
        self._dataSource.moveDown(index.row())
        self.layoutChanged.emit()

        return True

    def removeRow(self, row: int, parent: QModelIndex = ...) -> bool:
        self.beginRemoveRows(QModelIndex(), row, row)
        self._dataSource.delete(row)
        self.endRemoveRows()
        return True

    def copyRow(self, index: QModelIndex) -> None:
        self.layoutAboutToBeChanged.emit()
        self._dataSource.copy(index.row() + 1, index.row())
        self.layoutChanged.emit()

    def selectRow(self, index: QModelIndex) -> None:
        self._dataSource.select(index.row())

    def mimeTypes(self) -> typing.List[str]:
        return ["application/puppet-framedata"]

    def mimeData(self, indexes: typing.Iterable[QModelIndex]) -> "QMimeData":
        encode = []
        encode.append(list(indexes)[0].row())

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
        data: "QMimeData",
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
                self._dataSource.moveTo(parent.row(), int(decoded[0]))
                self.layoutChanged.emit()

            elif action == Qt.CopyAction:
                self.layoutAboutToBeChanged.emit()
                self._dataSource.copy(parent.row(), int(decoded[0]))
                self.layoutChanged.emit()

            return True

        return False

    @pyqtSlot(list)
    def dataSourceChanged(
        self, modelIndexes: typing.List[typing.Tuple[int, int]]
    ) -> None:
        for row, col in modelIndexes:
            index = self.index(row, col, QModelIndex())
            self.dataChanged.emit(
                index, index, [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole]
            )
