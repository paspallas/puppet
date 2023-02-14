from PyQt5.QtCore import QCoreApplication, QObject, Qt, pyqtSlot
from PyQt5.QtWidgets import QGraphicsItem, QProgressDialog

from ..gui.dialog import OpenImageDialog
from ..model.animation_frame import FrameSprite
from ..model.document import Document
from ..model.spritesheet import Sprite, SpriteSheetCollectionModel


class SpritePaletteController(QObject):
    def __init__(self, document: Document):
        super().__init__()

        self._document: Document = document

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

                self._document.spriteSheets().addSpriteSheet(path)
                QCoreApplication.instance().processEvents()

                if progress.wasCanceled():
                    return

            progress.setValue(len(paths))

    @pyqtSlot(str)
    def delSpriteSheet(self, id: str) -> None:
        self._document.spriteSheets().delSpriteSheet(id)

    @pyqtSlot(QGraphicsItem)
    def selectedSprite(self, sprite: Sprite) -> None:
        # TODO remember to change when the document changes
        self._document._currentEditableFrame.fromPixmap(sprite._pixmap)
