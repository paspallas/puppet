import typing


class Publisher:
    def __init__(self) -> None:
        self._subscribers: typing.Dict[int, typing.List[typing.Callable]] = dict()
        self._notify = True

    def subscribe(self, event: int, callback: typing.Callable) -> None:
        if not callable(callback):
            raise ValueError("Callback must be a callable object")

        if event not in self._subscribers.keys():
            self._subscribers[event] = [callback]
        else:
            self._subscribers[event].append(callback)

    def publish(self, event: int, *args: typing.Any) -> None:
        if not self._notify:
            return

        if event in self._subscribers.keys():
            for callback in self._subscribers[event]:
                callback(*args)

    def setNotify(self, value: bool) -> None:
        self._notify = value
