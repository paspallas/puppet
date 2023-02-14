from PyQt5.QtCore import QFileInfo, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QLabel, QVBoxLayout, QWidget


class OpenImageDialog(QFileDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setOption(QFileDialog.DontUseNativeDialog, True)
        self.setFileMode(QFileDialog.ExistingFiles)
        self.setFixedSize(self.width() + 250, self.height())

        self._ui_previewLbl = QLabel("Preview", self)
        self._ui_previewLbl.setFixedSize(250, 250)
        self._ui_previewLbl.setAlignment(Qt.AlignCenter)

        box = QVBoxLayout()
        box.addWidget(self._ui_previewLbl)
        box.addStretch()

        self.layout().addLayout(box, 1, 3, 1, 1)

        self.currentChanged.connect(self._onChange)
        self.fileSelected.connect(self._onFileSelected)
        self.filesSelected.connect(self._onFilesSelected)

        self._fileSelected = None
        self._filesSelected = None

    def _onChange(self, path: str):
        pixmap = QPixmap(path)

        if pixmap.isNull():
            self._ui_previewLbl.setText("Preview")
        else:
            self._ui_previewLbl.setPixmap(
                pixmap.scaled(
                    self._ui_previewLbl.width(),
                    self._ui_previewLbl.height(),
                    Qt.KeepAspectRatio,
                    Qt.FastTransformation,
                )
            )

    def _onFileSelected(self, file: str):
        self._fileSelected = file

    def _onFilesSelected(self, files: [str]):
        self._filesSelected = files

    def getFileSelected(self) -> str:
        return self._fileSelected

    def getFilesSelected(self) -> [str]:
        return self._filesSelected
