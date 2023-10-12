class Publisher:
    def __init__(self):
        self._subscribers: dict(str, [callable]) = dict()

    def subscribe(self, event: str, callback: callable) -> None:
        if not callable(callback):
            raise ValueError("Callback must be a callable object")

        if event is None or event == "":
            raise ValueError("Event id can't be empty")

        if event not in self._subscribers.keys():
            self._subscribers[event] = [callback]
        else:
            self._subscribers[event].append(callback)

    def publish(self, event, args):
        if event in self._subscribers.keys():
            for callback in self._subscribers[event]:
                callback(args)


class Subject(Publisher):
    def __init__(self):
        super().__init__()

        self._x: int = 0
        self._y: int = 0

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self.publish("xchanged", self._x)

    @property
    def y(self) -> int:
        return self._y

    @x.setter
    def y(self, value):
        self._y = value
        self.publish("ychanged", self._y)


class Observer:
    def getX(self, value):
        print(f"x has changed: value {value}")

    def getY(self, value):
        print(f"y has changed: value {value}")


def main():
    observerA = Observer()
    observerB = Observer()

    subject = Subject()
    subject.subscribe("xchanged", observerA.getX)
    subject.subscribe("ychanged", observerB.getY)
    subject.subscribe("", observerB.getX)

    subject.x = 9
    subject.x = 100
    subject.y = 120


if __name__ == "__main__":
    main()
