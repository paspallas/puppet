import typing

from ..model.animation_frame import FrameSprite, FrameSpriteItem


class SpriteStack:
    """Stack of sprites that represent the current sprite z ordering
    Guarantees that the contents are rendered in the correct order when
    a QTreeView is used for visualization.
    """

    def __init__(self) -> None:
        self._data: typing.List[FrameSprite] = list()

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, model_index: int) -> FrameSprite:
        return self._data[self._translateIndex(model_index)]

    def push(self, sprite: FrameSprite) -> None:
        sprite.z = len(self._data)
        self._data.append(sprite)

    def pop(self, model_index: int) -> FrameSprite:
        self._data.pop(self._translateIndex(model_index))
        self._updateZindex()

    def inc(self, model_index: int) -> None:
        if len(self._data) == 1:
            raise IndexError("The sprite stack has only one element")

        index = self._translateIndex(model_index)
        sprite = self._data.pop(index)
        self._data.insert(index + 1, sprite)
        self._updateZindex()

    def dec(self, model_index: int) -> None:
        if len(self._data) == 1:
            raise IndexError("The sprite stack has only one element")

        index = self._translateIndex(model_index)
        sprite = self._data.pop(index)
        self._data.insert(index - 1, sprite)
        self._updateZindex()

    def move(self, model_index_src: int, model_index_dst: int) -> None:
        src = self._translateIndex(model_index_src)
        dst = self._translateIndex(model_index_dst)
        sprite = self._data.pop(src)
        self._data.insert(dst, sprite)
        self._updateZindex()

    def _translateIndex(self, model_index: int) -> int:
        return len(self._data) - 1 - model_index

    def _updateZindex(self) -> None:
        for i, sprite in enumerate(self._data):
            sprite.z = i

    # @pyqtSlot(int)
    # def onIncreaseZ(self, z: int) -> None:
    #     if z + 1 > len(self) - 1:
    #         return

    #     self.sigFrameLayoutAboutToChange.emit()
    #     index = self.itemIndex(z)
    #     self.moveup(index)
    #     sprite = self.sprites[index - 1]
    #     self.sigFrameLayoutChanged.emit()

    #     self.sigSelectedItem.emit(self.itemIndex(sprite.z))

    # @pyqtSlot(int)
    # def onDecreaseZ(self, z: int) -> None:
    #     if z - 1 < 0:
    #         return

    #     self.sigFrameLayoutAboutToChange.emit()
    #     index = self.itemIndex(z)
    #     self.movedown(index)
    #     sprite = self.sprites[index + 1]
    #     self.sigFrameLayoutChanged.emit()

    #     self.sigSelectedItem.emit(self.itemIndex(sprite.z))
