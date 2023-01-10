from PyQt5.QtCore import QObject, pyqtSlot

from ..model.spritegroup import SpriteGroup, SpriteGroupCollectionModel
from ..model.spritesheet import SpriteSheet


class SpriteGroupController(QObject):
    """Control operations over a spritegroup that has been added to a spritepalette"""

    def __init__(self, model: SpriteGroupCollectionModel):
        super().__init__()

        self._model = model

    @pyqtSlot(SpriteSheet)
    def addGroup(self, sheet: SpriteSheet) -> None:
        """Add a new group to the collection created from a spritesheet

        Args:
            sheet (SpriteSheet)
        """
        group = SpriteGroup.fromSpriteSheet(sheet)

        # position the sprites in it's internally stored coordinates
        group.resetPos()
        group.lock()
        group.show()

        self._model.addGroup(group, sheet.name)

    @pyqtSlot(str)
    def delGroup(self, id: str) -> None:
        """Delete a group from the model

        Args:
            id (str): group id
        """
        self._model.hideGroup(id)
        self._model.delGroup(id)

    @pyqtSlot(str)
    def showGroup(self, id: str):
        """Show a single group in the scene

        Args:
            id (str): group id
        """
        self._model.showGroup(id)
