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

from .track import Track


class TrackModel(QAbstractItemModel):
    """Interface between the view and the collection of tracks of animation"""

    def __init__(self):
        super().__init__()

        self._dataSource: Track = None

        self.rootItem = Track([], None)
        for c in ["head", "torso", "front_leg"]:
            child = Track([c, ""], self.rootItem)
            self.rootItem.appendChild(child)

        parent = self.rootItem.childItems[1]
        translation = Track(["Translation", 10], parent)
        rotation = Track(["Rotation", 60], parent)
        parent.appendChild(translation)
        parent.appendChild(rotation)

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
            item = index.internalPointer()
            return item.data[index.column()]

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
        #! for different column counts invalidate the model index when needed
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.childItems[row]
        if childItem:
            return self.createIndex(row, column, childItem)
        return QModelIndex()

    def rowCount(self, parent: QModelIndex = ...) -> int:
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return len(parentItem.childItems)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 2

    def parent(self, index: QModelIndex) -> QModelIndex:
        if not index.isValid():
            return QModelIndex()

        parentItem = index.internalPointer().parentItem
        if parentItem == self.rootItem:
            return QModelIndex()
        return self.createIndex(parentItem.row(), 0, parentItem)

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
