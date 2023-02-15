import typing

from ..model.animation_frame.frame_sprite import FrameSprite


class SpriteStack:
    """Stack of sprites that represent the current sprite z ordering.

    Maps QModelIndexes between the stack indexes and QAbstractItemModel.

    Guarantees that the contents are rendered in the correct order when
    a QTreeView is used for visualization.
    """

    def __init__(self) -> None:
        self._data: typing.List[FrameSprite] = list()

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, model_index: int) -> FrameSprite:
        return self._data[self.spriteIndex(model_index)]

    def __iter__(self):
        self._currentIndex = 0
        return self

    def __next__(self):
        if self._currentIndex < len(self._data):
            sprite = self._data[self._currentIndex]
            self._currentIndex += 1
            return sprite
        raise StopIteration

    def push(self, sprite: FrameSprite) -> None:
        sprite.z = len(self._data)
        self._data.append(sprite)

    def pop(self, model_index: int) -> FrameSprite:
        sprite = self._data.pop(self.spriteIndex(model_index))
        self._updateZindex()
        return sprite

    def inc(self, model_index: int) -> None:
        if len(self._data) == 1:
            raise IndexError("The sprite stack has only one element")

        self.spriteUp(self.spriteIndex(model_index))

    def dec(self, model_index: int) -> None:
        if len(self._data) == 1:
            raise IndexError("The sprite stack has only one element")

        self.spriteDown(self.spriteIndex(model_index))

    def move(self, model_index_src: int, model_index_dst: int) -> None:
        src = self.spriteIndex(model_index_src)
        dst = self.spriteIndex(model_index_dst)

        sprite = self._data.pop(src)
        self._data.insert(dst, sprite)
        self._updateZindex()

    def insert(self, model_index: int, sprite: FrameSprite) -> None:
        self._data.insert(self.spriteIndex(model_index), sprite)
        self._updateZindex()

    def last(self) -> int:
        return len(self._data) - 1

    def spriteIndex(self, model_index: int) -> int:
        return len(self._data) - 1 - model_index

    def modelIndex(self, sprite_index: int) -> int:
        return self.spriteIndex(sprite_index)

    def _updateZindex(self) -> None:
        for i, sprite in enumerate(self._data):
            sprite.z = i

    def spriteUp(self, sprite_index: int) -> None:
        sprite = self._data.pop(sprite_index)
        self._data.insert(sprite_index + 1, sprite)
        self._updateZindex()

    def spriteDown(self, sprite_index: int) -> None:
        sprite = self._data.pop(sprite_index)
        self._data.insert(sprite_index - 1, sprite)
        self._updateZindex()
