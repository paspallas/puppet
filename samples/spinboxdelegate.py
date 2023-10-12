import sys

from PyQt5.QtWidgets import QApplication, QStyledItemDelegate, QSpinBox, QTableView
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtCore import Qt, QModelIndex


class SpinBoxDelegate(QStyledItemDelegate):
    """A delegate that allows the user to change integer values from the model
    using a spin box widget."""

    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        editor = QSpinBox(parent)
        editor.setFrame(False)
        editor.setMinimum(0)
        editor.setMaximum(100)
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        editor.setValue(value)

    def setModelData(self, editor, model, index):
        editor.interpretText()
        value = editor.value()
        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    model = QStandardItemModel(4, 2)
    tableView = QTableView()
    tableView.setModel(model)

    delegate = SpinBoxDelegate()
    tableView.setItemDelegate(delegate)
    tableView.horizontalHeader().setStretchLastSection(True)

    for row in range(4):
        for column in range(2):
            index = model.index(row, column, QModelIndex())
            value = (row + 1) * (column + 1)
            model.setData(index, value)

    tableView.setWindowTitle("Spin Box Delegate")
    tableView.show()
    sys.exit(app.exec())
