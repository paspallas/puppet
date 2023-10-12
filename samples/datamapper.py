import sys

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QDataWidgetMapper,
    QPushButton,
    QLineEdit,
    QTextEdit,
    QSpinBox,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QWidget,
)


class Widget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._nameLbl = QLabel("Name", self)
        self._nameEdit = QLineEdit(self)
        self._nameLbl.setBuddy(self._nameEdit)

        self._addressLbl = QLabel("Address", self)
        self._addressEdit = QTextEdit(self)
        self._addressLbl.setBuddy(self._addressEdit)

        self._ageLbl = QLabel("Age (in years)", self)
        self._ageSpin = QSpinBox(self)
        self._ageLbl.setBuddy(self._ageLbl)

        self._nextBtn = QPushButton("Next")
        self._prevBtn = QPushButton("Prev")

        h1 = QHBoxLayout()
        h1.addWidget(self._nameLbl, 1)
        h1.addWidget(self._nameEdit, 2)

        h2 = QHBoxLayout()
        h2.addWidget(self._addressLbl, 1)
        h2.addWidget(self._addressEdit, 2)

        h3 = QHBoxLayout()
        h3.addWidget(self._ageLbl, 1)
        h3.addWidget(self._ageSpin, 2)

        h4 = QHBoxLayout()
        h4.addStretch()
        h4.addWidget(self._prevBtn)
        h4.addWidget(self._nextBtn)

        editable = QVBoxLayout(self)
        editable.addLayout(h1)
        editable.addLayout(h2)
        editable.addLayout(h3)
        editable.addSpacing(20)
        editable.addLayout(h4)

        self.setModel()
        self._mapper = QDataWidgetMapper(self)
        self._mapper.setModel(self.model)
        self._mapper.addMapping(self._nameEdit, 0)
        self._mapper.addMapping(self._addressEdit, 1)
        self._mapper.addMapping(self._ageSpin, 2)
        self._prevBtn.clicked.connect(self._mapper.toPrevious)
        self._nextBtn.clicked.connect(self._mapper.toNext)
        self._mapper.currentIndexChanged.connect(self.updateButtons)
        self._mapper.toFirst()

    def updateButtons(self, row):
        self._prevBtn.setEnabled(row > 0)
        self._nextBtn.setEnabled(row < self.model.rowCount() - 1)

    def setModel(self):
        self.model = QStandardItemModel(3, 3, self)
        names = ["mario", "ana", "pablo"]
        addresses = ["xestoso 12", "pizarro 87", "gorxal 13"]
        ages = ["73", "68", "39"]

        for row in range(0, 3):
            item = QStandardItem(names[row])
            self.model.setItem(row, 0, item)
            item = QStandardItem(addresses[row])
            self.model.setItem(row, 1, item)
            item = QStandardItem(ages[row])
            self.model.setItem(row, 2, item)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Widget mapper example")

        self._edit = Widget()
        self.setCentralWidget(self._edit)


def main():
    app = QApplication([])
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
