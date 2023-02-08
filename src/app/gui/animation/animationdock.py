from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QModelIndex
from PyQt5.QtWidgets import QDockWidget, QWidget

from ...model.chardocument import CharDocument
from ...model.animation.animation_list_model import AnimationListModel
from ...model.animation.animation_list import AnimationList
from ...model.animation.animation_model import AnimationModel

from .animation_ui import AnimationUi


class AnimationEditorDock(QDockWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Animation")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAllowedAreas(Qt.BottomDockWidgetArea)

        self._container = QWidget(self)
        self.setWidget(self._container)

        self._ui = AnimationUi()
        self._ui.setupUi(self._container)

        # TODO move to document model
        self._model = AnimationListModel()
        self._sourceData = AnimationList()
        self._model.setDataSource(self._sourceData)
        self._ui.animationList.setModel(self._model)

        self._animationModel = AnimationModel()
        self._ui.frameList.setModel(self._animationModel)

        # self._framemodel.setDataSource(self._frameSourceData)

        self._ui.addAnimationBtn.clicked.connect(lambda: self._model.addItem())
        self._ui.deleteAnimationBtn.clicked.connect(self.onDeleteAnimation)
        self._ui.addFrameBtn.clicked.connect(lambda: self._animationModel.addItem())
        self._ui.deleteFrameBtn.clicked.connect(self.onDeleteFrame)
        self._ui.animationList.clicked.connect(self.onAnimationClicked)

    @pyqtSlot(QModelIndex)
    def onAnimationClicked(self, index: QModelIndex) -> None:
        item = self._ui.animationList.model().itemFromIndex(index)
        # use this as a key into a dictionary
        print(f"new animation model data source {item.value()}")
        self._animationModel.setDataSource(self._sourceData.source(item.value()))

    @pyqtSlot()
    def onDeleteAnimation(self) -> None:
        index = self._ui.animationList.currentIndex()
        print(index.row())
        if index.isValid():
            self._model.delItem(index.row())

    @pyqtSlot()
    def onDeleteFrame(self) -> None:
        index = self._ui.frameList.currentIndex()
        print(index.row())
        if index.isValid():
            self._animationModel.delItem(index.row())
