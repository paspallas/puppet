from PyQt5.QtCore import QModelIndex, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QDockWidget, QWidget

from ...model.document import Document
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

    def setDocument(self, document: Document) -> None:
        self._document = document

        self._ui.animationList.setModel(self._document.animationListModel())
        self._ui.frameList.setModel(self._document.animationModel())

        self._ui.addAnimationBtn.clicked.connect(
            lambda: self._document.animationListModel().addItem()
        )
        self._ui.deleteAnimationBtn.clicked.connect(self.onDeleteAnimation)
        self._ui.addFrameBtn.clicked.connect(
            lambda: self._document.animationModel().addItem()
        )
        self._ui.deleteFrameBtn.clicked.connect(self.onDeleteFrame)
        self._ui.animationList.clicked.connect(self.onAnimationClicked)

    @pyqtSlot(QModelIndex)
    def onAnimationClicked(self, index: QModelIndex) -> None:
        item = self._ui.animationList.model().itemFromIndex(index)
        self._document.animationModel().setDataSource(
            self._document.animationList().source(item.value())
        )

    @pyqtSlot()
    def onDeleteAnimation(self) -> None:
        index = self._ui.animationList.currentIndex()
        if index.isValid():
            self._ui.animationList.model().delItem(index.row())

    @pyqtSlot()
    def onDeleteFrame(self) -> None:
        index = self._ui.frameList.currentIndex()
        if index.isValid():
            self._ui.frameList.model().delItem(index.row())
