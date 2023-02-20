import pickle
import typing

from PyQt5.QtCore import (
    QAbstractItemModel,
    QMimeData,
    QModelIndex,
    QSize,
    Qt,
    QVariant,
    pyqtSignal,
    pyqtSlot,
)

from track import Track


class TrackModel(QAbstractItemModel):
    """Interface between the view and the collection of tracks of animation"""

    def __init__(self):
        super().__init__()

        self._dataSource: Track = None

    # def setDataSource(self, source: AnimationFrame) -> None:
    #     self.beginResetModel()

    #     if self._dataSource is not None:
    #         self._dataSource.sigFrameDataChanged.disconnect()
    #         self._dataSource.sigFrameLayoutChanged.disconnect()

    #     self._dataSource = source
    #     self._dataSource.sigAddedItem.connect(self.newRow)
    #     self._dataSource.sigFrameDataChanged.connect(self.dataSourceChanged)
    #     self._dataSource.sigFrameLayoutAboutToChange.connect(
    #         lambda: self.layoutAboutToBeChanged.emit()
    #     )
    #     self._dataSource.sigFrameLayoutChanged.connect(
    #         lambda: self.layoutChanged.emit()
    #     )

    #     self.endResetModel()

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if not index.isValid():
            return QVariant()

        if role in [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole]:
            return "Test Track"
            return QVariant(self._dataSource.get(index.row(), index.column()))

        if role == Qt.ItemDataRole.SizeHintRole:
            return QSize(0, 20)

        # if role == Qt.ItemDataRole.CheckStateRole and index.column() in [
        #     Index.Hide,
        #     Index.Lock,
        # ]:
        #     return QVariant(self._dataSource.get(index.row(), index.column()))

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

        # if index.column() in [Index.Hide, Index.Lock]:
        #     return flags | Qt.ItemIsUserCheckable

        return flags

    def index(self, row: int, column: int, parent: QModelIndex = ...) -> QModelIndex:
        if row < 0 or row >= 1:
            return QModelIndex()
        return self.createIndex(row, column)

    def rowCount(self, parent: QModelIndex = ...) -> int:
        if parent.isValid():
            return 0

        return 1
        # return len(self._dataSource)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 1

    def parent(self, child: QModelIndex) -> QModelIndex:
        return QModelIndex()

    def newRow(self) -> None:
        self.beginInsertRows(QModelIndex(), 0, 0)
        self.endInsertRows()

    def removeRow(self, row: int, parent: QModelIndex = ...) -> bool:
        self.beginRemoveRows(QModelIndex(), row, row)
        self._dataSource.delete(row)
        self.endRemoveRows()
        return True

    def selectRow(self, index: QModelIndex) -> None:
        self._dataSource.select(index.row())

    # @pyqtSlot(list)
    # def dataSourceChanged(
    #     self, modelIndexes: typing.List[typing.Tuple[int, int]]
    # ) -> None:
    #     for row, col in modelIndexes:
    #         index = self.index(row, col, QModelIndex())
    #         self.dataChanged.emit(
    #             index, index, [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole]
    #         )
