from .sprite import Sprite
from .spritesheet import SpriteSheet


class SpriteGroup:
    """Collection of sprite objects.
    Represents a view of the sprites to be used in an editor
    """

    def __init__(self, sprites: list[Sprite]):
        self._sprites = sprites

    @staticmethod
    def fromSpriteSheet(sheet: SpriteSheet):
        return SpriteGroup(sheet.sprites())

    def add(self, sprite: Sprite) -> None:
        self._sprites.append(sprite)

    def extend(self, sprites: list[Sprite]) -> None:
        self._sprites.extend(sprites)

    def hide(self) -> None:
        for sprite in self._sprites:
            sprite.hide()

    def show(self) -> None:
        for sprite in self._sprites:
            sprite.show()

    def resetPos(self) -> None:
        for sprite in self._sprites:
            sprite.setPos(sprite.x, sprite.y)

    def lock(self) -> None:
        for sprite in self._sprites:
            sprite.lock()

    def unlock(self) -> None:
        for sprite in self._sprites:
            sprite.unlock()

    def __iter__(self):
        self._currentIndex = 0
        return self

    def __next__(self):
        if self._currentIndex < len(self._sprites):
            sprite = self._sprites[self._currentIndex]
            self._currentIndex += 1
            return sprite
        raise StopIteration
