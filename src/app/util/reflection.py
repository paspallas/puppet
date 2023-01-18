import inspect


class PropertyList:
    """Collect properties declared in a given class.

    Provides a way to access class instance properties by index.
    Useful for streamlining QAbtractItemModel access to the underliying data.
    """

    def __init__(self, cls):
        self._properties: list[str] = list()
        self.__properties(cls)

    def count(self) -> int:
        return len(self._properties)

    def __properties(self, cls):
        """Build a list of methods names of the given class
        decorated with @property.
        """
        lines = inspect.getsourcelines(cls)[0]

        for i, line in enumerate(lines):
            line = line.strip()

            if line.split("(")[0].strip() == "@property":
                nextLine = lines[i + 1]
                name = nextLine.split("def")[1].split("(")[0].strip()
                self._properties.append(name)

    def __getitem__(self, index: int) -> str:
        return self._properties[index]
