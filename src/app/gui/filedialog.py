from PyQt5.QtCore import QFileInfo, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QLabel, QVBoxLayout, QWidget


class DialogFileIO:
    """Utility class to simplify FileIO"""

    @staticmethod
    def openFiles(parent: QWidget, filter: str, hint: str = "Open file") -> [str]:
        paths, _ = QFileDialog.getOpenFileNames(
            parent,
            hint,
            "",
            filter=filter,
            options=QFileDialog.DontUseNativeDialog,
        )

        if len(paths) > 0:
            return paths
        return None

    @staticmethod
    def saveFile(parent: QWidget, filter: str, hint: str = "Save file") -> (str, str):
        path, _ = QFileDialog.getSaveFileName(
            parent,
            hint,
            "",
            filter=filter,
            options=QFileDialog.DontUseNativeDialog,
        )

        if path and len(path) > 0:
            return path, QFileInfo(path).fileName()
        return None, None


class DialogPreviewImage(QFileDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setOption(QFileDialog.DontUseNativeDialog, True)
        self.setFileMode(QFileDialog.ExistingFiles)
        self.setFixedSize(self.width() + 250, self.height())

        self._preview = QLabel("Preview", self)
        self._preview.setFixedSize(250, 250)
        self._preview.setAlignment(Qt.AlignCenter)

        box = QVBoxLayout()
        box.addWidget(self._preview)
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
            self._preview.setText("Preview")
        else:
            self._preview.setPixmap(
                pixmap.scaled(
                    self._preview.width(),
                    self._preview.height(),
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
