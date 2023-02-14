from importlib import import_module as imodule

from PyQt5.QtCore import QCoreApplication, QEvent, QObject, Qt, pyqtSlot
from PyQt5.QtWidgets import QGraphicsScene

from .abstract_tool import AbstractTool


class SceneToolManager(QObject):
    """Manage tool operations in the graphics scene"""

    def __init__(self, scene: QGraphicsScene):
        super().__init__(scene)

        self._tool: AbstractTool = None
        scene.installEventFilter(self)

    def eventFilter(self, obj: QObject, e: QEvent) -> bool:
        scene: QGraphicsScene = obj

        if scene is None:
            return super().eventFilter(obj, e)

        if e.type() == QEvent.GraphicsSceneMousePress:
            if self._tool is not None:
                self._tool.onMousePress(e)
            return False

        elif e.type() == QEvent.GraphicsSceneMouseMove:
            if self._tool is not None:
                self._tool.onMouseMove(e)
            return False

        elif e.type() == QEvent.GraphicsSceneMouseRelease:
            if self._tool is not None:
                self._tool.onMouseRelease(e)
            return False

        return super().eventFilter(obj, e)

    def setTool(self, tool_cls: str, activate: bool) -> None:
        if self._tool is not None:
            self._tool.disable()
            self._tool = None

            if activate:
                try:
                    toolCls = getattr(imodule(f"app.tool.{tool_cls}".lower()), tool_cls)
                    self._tool = toolCls(scene=self.parent())
                    self._tool.enable()
                except AttributeError as e:
                    print(e)
