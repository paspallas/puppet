import typing

from ..frame_sprite import FrameSprite

__alpha__ = []


class HighLightSelected:
    @staticmethod
    def apply(items: typing.List[FrameSprite], selected: int) -> None:
        if len(items) > 1:
            for i, item in enumerate(items):
                __alpha__.append(item.alpha)

                if i < selected:
                    item.alpha = 70

    @staticmethod
    def revert(items: typing.List[FrameSprite]) -> None:
        for i, item in enumerate(items):
            item.alpha = __alpha__[i]

        __alpha__.clear()
