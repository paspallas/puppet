import typing

from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QVariant

from .animation import Animation


class AnimationModel(QAbstractListModel):
    """Interface between the listview and the current animation"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._dataSource: Animation = None

    def setDataSource(self, source: Animation) -> None:
        self.beginResetModel()
        self._dataSource = source
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()) -> int:
        if self._dataSource is not None:
            return len(self._dataSource)
        return 0

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if not index.isValid():
            return QVariant()

        if role in [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole]:
            return QVariant(self._dataSource.get(index.row()))

        return QVariant()

    def addItem(self) -> None:
        self.layoutAboutToBeChanged.emit()
        self._dataSource.add()
        self.layoutChanged.emit()

    def delItem(self, index: int) -> None:
        self.layoutAboutToBeChanged.emit()
        self._dataSource.delete(index)
        self.layoutChanged.emit()

    # def itemFromIndex(self, index: QModelIndex) -> QVariant:
    #     return QVariant(self._dataSource[index.row()])
