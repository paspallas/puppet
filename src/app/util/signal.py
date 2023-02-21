import typing

from PyQt5.QtCore import QMetaMethod, QObject


def getSignal(obj: QObject, signalName: str) -> typing.Any:
    metaObj = obj.metaObject()
    for i in range(metaObj.methodCount()):
        metaMethod = metaObj.method(i)
        if not metaMethod.isValid():
            continue
        if (
            metaMethod.methodType() == QMetaMethod.Signal
            and metaMethod.name() == signalName
        ):
            return metaMethod

    return None
