import typing

# an animation has a collection of keyframes,
# the character has a collection of tracks, one for each sprite


class KeyFrame:
    def __init__(self) -> None:
        self.start = 0
        self.end = 0


# maybe an abstract base class?
class TrackProperty:
    def __init__(self) -> None:
        self._keyframes = []


class Track:
    def __init__(self, data, parent=None) -> None:
        self.parentItem = parent
        self.data = data
        self.childItems = []

    def appendChild(self, item) -> None:
        self.childItems.append(item)

    def row(self) -> int:
        if self.parentItem:
            return self.parentItem.childItems.index(self)

        # I'm the parent
        return 0
