import typing

from PyQt5.QtWidgets import QGraphicsScene, QGraphicsSceneMouseEvent

from .abstract_tool import AbstractTool


class EditBone(AbstractTool):
    def __init__(self, scene: QGraphicsScene) -> None:
        super().__init__(scene)

    def enable(self) -> None:
        pass

    def onMouseMove(self, e: QGraphicsSceneMouseEvent) -> None:
        pass

    def onMousePress(self, e: QGraphicsSceneMouseEvent) -> None:
        pass

    def onMouseRelease(self, e: QGraphicsSceneMouseEvent) -> None:
        pass
