from PyQt5.QtCore import QAbstractItemModel, QModelIndex, Qt, QVariant, pyqtSlot
from PyQt5.QtGui import QMouseEvent, QPaintEvent, QWheelEvent
from PyQt5.QtWidgets import QDataWidgetMapper, QWidget

from ...model.animation_frame import AnimationFrameModel
from .. import style
from .sprite_property_ui import SpritePropertyUi


class SpritePropertyWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self._ui = SpritePropertyUi()
        self._ui.setupUi(self)
        self._mapper = QDataWidgetMapper(self)
        self._model: AnimationFrameModel = None
        # self.setEnabled(False)

    def setModel(self, model) -> None:
        self._model = model
        self._mapper.setModel(model)
        self.setMapper()

    def setMapper(self) -> None:
        self._mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self._mapper.addMapping(self._ui.xSpin, 3)
        self._mapper.addMapping(self._ui.ySpin, 4)
        self._mapper.addMapping(self._ui.opacitySlide, 5)
        self._mapper.addMapping(self._ui.flipHorizontalChk, 6)
        self._mapper.addMapping(self._ui.flipVerticalChk, 7)

        self._ui.xSpin.valueChanged.connect(self._mapper.submit, Qt.QueuedConnection)
        self._ui.ySpin.valueChanged.connect(self._mapper.submit, Qt.QueuedConnection)
        self._ui.opacitySlide.valueChanged.connect(
            self._mapper.submit, Qt.QueuedConnection
        )
        self._ui.flipHorizontalChk.stateChanged.connect(
            self._mapper.submit, Qt.QueuedConnection
        )
        self._ui.flipVerticalChk.stateChanged.connect(
            self._mapper.submit, Qt.QueuedConnection
        )

    @pyqtSlot(QModelIndex)
    def onSelectedItemChanged(self, index: QModelIndex) -> None:
        self._mapper.setCurrentModelIndex(index)

    @pyqtSlot(bool)
    def setEnabled(self, enabled: bool) -> None:
        super().setEnabled(enabled)

    def paintEvent(self, e: QPaintEvent) -> None:
        style.paintWidget(self)

    # We don't want the scene to receive mouse events
    def mousePressEvent(self, e: QMouseEvent) -> None:
        e.accept()

    def wheelEvent(self, e: QWheelEvent) -> None:
        e.accept()
