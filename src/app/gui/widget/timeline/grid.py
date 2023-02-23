import typing

from PyQt5.QtCore import QLineF, QRectF, Qt
from PyQt5.QtGui import QColor, QPainter, QPen

__pxPerFrame__ = 10
__xoffset__ = 20
__yoffset__ = 70

__trackHeight__ = 20
__trackVSpacing__ = 8
__innerTrackSpacing__ = 5
__subTrackVSpacing__ = 3

__pencolor__ = QColor(30, 30, 30)
__lightBrush__ = QColor(100, 100, 100)
__darkBrush__ = QColor(72, 72, 72)

__lightRects__: typing.List[QRectF] = []
__darkRects__: typing.List[QRectF] = []


class Grid:
    @staticmethod
    def computeGrid(sceneRect: QRectF, itemsPerTrack: typing.List[int]) -> None:
        __lightRects__.clear()
        __darkRects__.clear()

        left = int(sceneRect.left() - (sceneRect.left() % __pxPerFrame__)) + __xoffset__
        right = int(sceneRect.right())
        top = int(sceneRect.top() - sceneRect.top() % __trackHeight__) + __yoffset__
        bottom = int(sceneRect.bottom())

        start = top
        for nItems in itemsPerTrack:
            vSpacing = 0
            nSubTrack = 0
            totalTrackHeight = nItems * __trackHeight__
            end = start + totalTrackHeight

            for y in range(start, end, __trackHeight__):
                if nSubTrack > 0:
                    if nSubTrack == 1:
                        vSpacing += __innerTrackSpacing__
                        totalTrackHeight += __innerTrackSpacing__
                    else:
                        vSpacing += __subTrackVSpacing__
                        totalTrackHeight += __subTrackVSpacing__

                for x in range(left, right, __pxPerFrame__):
                    if nSubTrack % 2 == 0:
                        __darkRects__.append(
                            QRectF(x, y + vSpacing, __pxPerFrame__, __trackHeight__)
                        )
                    else:
                        __lightRects__.append(
                            QRectF(x, y + vSpacing, __pxPerFrame__, __trackHeight__)
                        )
                nSubTrack += 1

            # next parentTrack
            start += totalTrackHeight + __trackVSpacing__

    @staticmethod
    def paint(painter: QPainter) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(__pencolor__, 0, Qt.SolidLine, Qt.SquareCap)
        pen.setCosmetic(True)
        painter.setPen(pen)

        painter.setBrush(__darkBrush__)
        painter.drawRects(__darkRects__)
        painter.setBrush(__lightBrush__)
        painter.drawRects(__lightRects__)

    @staticmethod
    def alignTo(x: float, offset: float = 0) -> float:
        pos = round(x / __pxPerFrame__) * __pxPerFrame__
        if pos < __xoffset__:
            pos = __xoffset__

        return pos + offset
