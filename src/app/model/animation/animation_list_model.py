import typing

from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QVariant

from .animation_list import AnimationList


class AnimationListModel(QAbstractListModel):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def setDataSource(self, source: AnimationList) -> None:
        self._dataSource = source

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._dataSource)

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if not index.isValid():
            return QVariant()

        if role in [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole]:
            return QVariant(self._dataSource.get(index.row()))

        return QVariant()

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        if role == Qt.EditRole:
            self._dataSource.set(index.row(), value)
            self.dataChanged.emit(index, QModelIndex(), [])
            return True

        return False

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.NoItemFlags

        flags = Qt.ItemIsEditable | Qt.ItemIsEnabled | super().flags(index)

        return flags

    def itemFromIndex(self, index: QModelIndex) -> QVariant:
        return QVariant(self._dataSource.get(index.row()))

    def addItem(self) -> None:
        self.layoutAboutToBeChanged.emit()
        self._dataSource.add()
        self.layoutChanged.emit()

    def delItem(self, index: int) -> None:
        self.layoutAboutToBeChanged.emit()
        self._dataSource.delete(index)
        self.layoutChanged.emit()
