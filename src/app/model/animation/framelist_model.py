import typing

from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QVariant


class FrameListModel(QAbstractListModel):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def setDataSource(self, source: typing.List) -> None:
        self._dataSource = source

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._dataSource)

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if not index.isValid():
            return QVariant()

        if role in [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole]:
            return QVariant(self._dataSource[index.row()])

        return QVariant()

    # def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
    #     if role == Qt.EditRole:
    #         self._dataSource[index.row()] = value
    #         self.dataChanged.emit(index, QModelIndex(), [])
    #         return True

    #     return False

    def itemFromIndex(self, index: QModelIndex) -> QVariant:
        return QVariant(self._dataSource[index.row()])
