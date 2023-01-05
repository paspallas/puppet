from PyQt5.QtCore import QPoint, QRectF, QSize, QSizeF, Qt, pyqtSlot
from PyQt5.QtGui import QColor, QPainter, QPaintEvent
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QSizePolicy,
    QSlider,
    QSpacerItem,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from app.model.sprite import Sprite, SpriteObject


class PropertiesGroupBox(QGroupBox):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.setTitle("Sprite Properties")

        self.opacity = QSlider()
        self.opacity.setRange(0, 100)
        self.opacity.setValue(100)
        self.opacity.setOrientation(Qt.Horizontal)

        # self.l_rotate = QSpinBox()
        # self.l_rotate.setRange(0, 360)

        # self.r_rotate = QSpinBox()
        # self.r_rotate.setRange(0, 360)

        self.opacity_label = QLabel("opacity: ")
        # self.r_label = QLabel("rigth: ")

        layout = QVBoxLayout(self)

        l1 = QHBoxLayout()
        l1.setContentsMargins(0, 0, 0, 0)
        l1.addWidget(self.opacity_label)
        l1.addWidget(self.opacity)

        # l2 = QHBoxLayout()
        # l2.setContentsMargins(0, 0, 0, 0)
        # l2.addWidget(self.r_label)
        # l2.addWidget(self.r_rotate)

        layout.addLayout(l1)
        # layout.addLayout(l2)

        self.makeConnections()

    def makeConnections(self):
        self.opacity.valueChanged.connect(self.parent().handledItem.setOpacity)


class PropertyBox(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setMinimumSize(QSize(250, 64))

        self.background_color = QColor("#424242")
        self.foreground_color = QColor("#353535")
        self.border_radius = 4

        self.handledItem = SpriteObject()

        gr1 = PropertiesGroupBox(self)
        # gr2 = RotateGroupBox()
        # gr3 = RotateGroupBox()
        # gr4 = RotateGroupBox()

        layout = QVBoxLayout(self)
        layout.addWidget(gr1)
        # layout.addWidget(gr2)
        # layout.addWidget(gr3)
        # layout.addWidget(gr4)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(self.foreground_color)
        painter.setBrush(self.background_color)
        rect = QRectF(
            QPoint(), QSizeF(self.size() - 0.5 * painter.pen().width() * QSize(1, 1))
        )
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)

    @pyqtSlot(Sprite)
    def onSelectedItemChanged(self, item: Sprite):
        print("on sprite changed")
        self.handledItem.setSpriteItem(item)


class SpriteListBox(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self._setupUI()
        self._makeConnections()

        self._list.addItem("head")
        self._list.addItem("legs")
        self._list.addItem("hands")
        self._list.addItem("feet")
        self._list.addItem("body")

    def _setupUI(self) -> None:
        self.setMaximumSize(QSize(250, 300))

        self._list = QListWidget(self)
        self._list.setDragDropMode(QAbstractItemView.InternalMove)
        self._list.model().rowsMoved.connect(self._reorder)

        self._btnUp = QPushButton("+")
        self._btnDown = QPushButton("-")
        self._btnUp.setMaximumSize(QSize(32, 32))
        self._btnDown.setMaximumSize(QSize(32, 32))

        vbox = QVBoxLayout(self)
        vbox.addWidget(self._list)
        btnBox = QHBoxLayout()
        vbox.addLayout(btnBox)
        hspacer = QSpacerItem(64, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        btnBox.addWidget(self._btnUp, 0, Qt.AlignLeft)
        btnBox.addWidget(self._btnDown, 0, Qt.AlignLeft)
        btnBox.addItem(hspacer)

    def _makeConnections(self) -> None:
        self._btnUp.clicked.connect(self._moveSpriteUp)
        self._btnDown.clicked.connect(self._moveSpriteDown)

    @pyqtSlot()
    def _moveSpriteUp(self) -> None:
        row = self._list.currentRow()
        if row - 1 >= 0:
            self._swapItems(row, row - 1)

    @pyqtSlot()
    def _moveSpriteDown(self) -> None:
        row = self._list.currentRow()
        if row + 1 <= self._list.count() - 1:
            self._swapItems(row, row + 1)

    def _swapItems(self, row_1: int, row_2: int) -> None:
        # taking the item modifies the number of rows
        # get the second item first
        item2 = self._list.item(row_2)
        item1 = self._list.takeItem(row_1)

        self._list.insertItem(row_2, item1)
        self._list.setCurrentItem(item1)

        print(f"swap {item1.text()} with {item2.text()}")

        # TODO call method in frame container to swap z-indexes

    def _reorder(self) -> None:
        pass

    def paintEvent(self, e: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QColor("#424242"))
        painter.setBrush(QColor("#353535"))
        rect = QRectF(
            QPoint(), QSizeF(self.size() - 0.5 * painter.pen().width() * QSize(1, 1))
        )
        painter.drawRoundedRect(rect, 4, 4)


# FancySlider::FancySlider(QWidget * parent)
#     : QSlider(parent)
# {
# }

# FancySlider::FancySlider(Qt::Orientation orientation, QWidget * parent)
#     : QSlider(orientation, parent)
# {
# }

# void FancySlider::sliderChange(QAbstractSlider::SliderChange change)
# {
#     QSlider::sliderChange(change);

#     if (change == QAbstractSlider::SliderValueChange )
#     {
#         QStyleOptionSlider opt;
#         initStyleOption(&opt);

#         QRect sr = style()->subControlRect(QStyle::CC_Slider, &opt, QStyle::SC_SliderHandle, this);
#         QPoint bottomRightCorner = sr.bottomLeft();

#         QToolTip::showText(mapToGlobal( QPoint( bottomRightCorner.x(), bottomRightCorner.y() ) ), QString::number(value()), this);
#     }
# }
