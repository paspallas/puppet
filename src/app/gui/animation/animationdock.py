from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QModelIndex
from PyQt5.QtWidgets import QDockWidget, QWidget

from ...model.chardocument import CharDocument
from ...model.animation.animationlist_model import AnimationListModel
from ...model.animation.framelist_model import FrameListModel

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
        self._sourceData = ["walk", "Crouch", "Attack"]
        self._model.setDataSource(self._sourceData)
        self._ui.animationList.setModel(self._model)

        self._framemodel = FrameListModel()
        self._frameSourceData = ["walk_1", "walk_2", "walk_3"]
        self._framemodel.setDataSource(self._frameSourceData)
        self._ui.frameList.setModel(self._framemodel)

        self._ui.animationList.clicked.connect(self.onClicked)

    @pyqtSlot(QModelIndex)
    def onClicked(self, index: QModelIndex) -> None:
        item = self._ui.animationList.model().itemFromIndex(index)
        print(item.value())
