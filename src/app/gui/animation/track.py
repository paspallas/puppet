import typing


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
        return 0
    
    
