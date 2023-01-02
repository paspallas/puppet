from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QFileDialog


class DialogFileIO(QFileDialog):
    """Utility class to simplify FileIO"""

    def __init__(self):
        super().__init__()

        self._options = self.Options()
        self._options |= self.DontUseNativeDialog

    def openFile(self, filter: str) -> (str, str):
        path, _ = self.getOpenFileName(
            self, "Open File", "", filter=filter, options=self._options
        )

        if path and len(path) > 0:
            return path, QFileInfo(path).fileName()
        return None, None

    def saveFile(self, filter: str) -> (str, str):
        path, _ = self.getSaveFileName(
            self, "Save File", "", filter=filter, options=self._options
        )

        if path and len(path) > 0:
            return path, QFileInfo(path).fileName()
        return None, None
