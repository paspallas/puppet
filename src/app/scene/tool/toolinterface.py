from abc import ABC, ABCMeta, abstractmethod

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsScene, QGraphicsSceneMouseEvent


class AbstractTool:
    pass


class AbstractToolState(ABC):
    @property
    def tool(self) -> AbstractTool:
        return self._tool

    @tool.setter
    def tool(self, tool: AbstractTool) -> None:
        self._tool = tool

    def mouseMove(self, e: QGraphicsSceneMouseEvent) -> None:
        pass

    def mousePress(self, e: QGraphicsSceneMouseEvent) -> None:
        pass

    def mouseRelease(self, e: QGraphicsSceneMouseEvent) -> None:
        pass


class AbstractObject(ABCMeta, type(QObject)):
    pass


class AbstractTool(ABC, metaclass=AbstractObject):
    """Interface class for tools that perform operations on a QGraphicsScene"""

    def __init__(self, scene: QGraphicsScene = None):
        self._scene: QGraphicsScene = scene
        self._gizmo: QGraphicsItem = None
        self._state = AbstractToolState = None

    def transition(self, state: AbstractToolState) -> None:
        self._state = state
        self._state.tool = self

    @classmethod
    @abstractmethod
    def enable(self) -> None:
        pass

    def disable(self) -> None:
        self._state = None

    @classmethod
    @abstractmethod
    def onMouseMove(self, e: QGraphicsSceneMouseEvent) -> None:
        pass

    @classmethod
    @abstractmethod
    def onMousePress(self, e: QGraphicsSceneMouseEvent) -> None:
        pass

    @classmethod
    @abstractmethod
    def onMouseRelease(self, e: QGraphicsSceneMouseEvent) -> None:
        pass

    def onMouseDoubleClick(self, e: QGraphicsSceneMouseEvent) -> None:
        pass
