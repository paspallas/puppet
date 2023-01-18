import pickle
from typing import Any

from PyQt5.QtCore import QAbstractItemModel, QMimeData, QModelIndex, Qt, QVariant

from .animation_frame import AnimationFrame


class AnimationFrameModel(QAbstractItemModel):
    def __init__(self):
        super().__init__()

        self._dataSource: AnimationFrame = None

    def setDataSource(self, source: AnimationFrame) -> None:
        self._dataSource = source

    def data(self, index: QModelIndex, role: int):
        if not index.isValid():
            return QVariant()

        if role in [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole]:
            return QVariant(self._dataSource.get(index.row(), index.column()))

        if role == Qt.ItemDataRole.CheckStateRole and index.column() in [7, 8]:
            return QVariant(self._dataSource.get(index.row(), index.column()))

        return QVariant()

    def setData(self, index: QModelIndex, value: Any, role: int) -> bool:
        if role == Qt.EditRole:
            self._dataSource.set(index.row(), index.column(), value)
            self.dataChanged.emit(index, QModelIndex(), [])
            return True

        if role == Qt.CheckStateRole:
            self._dataSource.set(index.row(), index.column(), value)
            self.dataChanged.emit(index, QModelIndex(), [])
            return True

        return False

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
        if row < 0 or row >= len(self._dataSource):
            return QModelIndex()
        return self.createIndex(row, column)

    def rowCount(self, parent: QModelIndex) -> int:
        if parent.isValid():
            return 0
        return len(self._dataSource)

    def columnCount(self, parent: QModelIndex) -> int:
        return self._dataSource.count()

    def parent(self, index: QModelIndex) -> QModelIndex:
        return QModelIndex()

    def moveRowUp(self, index: QModelIndex) -> bool:
        if index.row() == 0:
            return False

        self.layoutAboutToBeChanged.emit()
        self._dataSource.moveup(index.row())
        self.layoutChanged.emit()
        return True

    def moveRowDown(self, index: QModelIndex) -> bool:
        if index.row() == len(self._dataSource) - 1:
            return False

        self.layoutAboutToBeChanged.emit()
        self._dataSource.movedown(index.row())
        self.layoutChanged.emit()
        return True

    def removeRow(self, row: int, parent: QModelIndex):
        self.beginRemoveRows(QModelIndex(), row, row)
        self._dataSource.deleteItem(row)
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
                self._dataSource.moveTo(parent.row(), int(decoded[0]))
                self.layoutChanged.emit()

            elif action == Qt.CopyAction:
                self.layoutAboutToBeChanged.emit()
                self._dataSource.copy(parent.row(), int(decoded[0]))
                self.layoutChanged.emit()

            return True

        return False
