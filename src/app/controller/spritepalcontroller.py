from PyQt5.QtCore import QCoreApplication, QObject, Qt, pyqtSlot
from PyQt5.QtWidgets import QGraphicsItem, QProgressDialog

from ..gui.dialog import OpenImageDialog
from ..model.sprite import Sprite
from ..model.spritesheet import SpriteSheetCollectionModel
from ..model.chardocument import CharDocument


class SpritePaletteController(QObject):
    def __init__(self, model: CharDocument):
        super().__init__()

        self._model = model

    @pyqtSlot()
    def addSpriteSheet(self) -> None:
        dialog = OpenImageDialog(None, "Open Images", "", "Sprite Sheet Images (*.png)")
        if dialog.exec() == OpenImageDialog.Accepted:
            paths = dialog.getFilesSelected()

            progress = QProgressDialog()
            progress.setMinimumDuration(0)
            progress.setWindowModality(Qt.WindowModal)
            progress.setWindowTitle("Import spritesheet")
            progress.setFixedSize(300, 150)
            progress.setCancelButtonText("Cancel")
            progress.setRange(0, len(paths))
            progress.show()

            for i, path in enumerate(paths):
                progress.setValue(i)
                progress.setLabelText(
                    f"Importing spritesheet {i + 1} of {len(paths)}..."
                )

                self._model.spriteSheets().addSpriteSheet(path)
                QCoreApplication.instance().processEvents()

                if progress.wasCanceled():
                    return

            progress.setValue(len(paths))

    @pyqtSlot(str)
    def delSpriteSheet(self, id: str) -> None:
        self._model.spriteSheets().delSpriteSheet(id)

    @pyqtSlot(QGraphicsItem)
    def selectedSprite(self, sprite: Sprite) -> None:
        self._model.addSprite(sprite.copy())
