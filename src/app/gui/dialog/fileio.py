from PyQt5.QtCore import QFileInfo, Qt
from PyQt5.QtWidgets import QFileDialog, QWidget


class FileIoDialog:
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
