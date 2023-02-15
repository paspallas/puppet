import typing

from ....collection import SpriteStack

__alpha__ = []


class HighLightSelected:
    @staticmethod
    def apply(sprites: SpriteStack, selected: int) -> None:
        if len(sprites) > 1:
            for i, sprite in enumerate(sprites):
                __alpha__.append(sprite.alpha)

                if i > selected:
                    sprite.alpha = 70

    @staticmethod
    def revert(sprites: SpriteStack) -> None:
        for i, sprite in enumerate(sprites):
            sprite.alpha = __alpha__[i]

        __alpha__.clear()
