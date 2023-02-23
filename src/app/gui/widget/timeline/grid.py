import typing

from PyQt5.QtCore import QLineF, QRectF, Qt
from PyQt5.QtGui import QColor, QPainter, QPen

__pxPerFrame__ = 10
__xoffset__ = 20
__yoffset__ = 70

__trackHeight__ = 20
__trackVSpacing__ = 6
__subTrackVSpacing__ = 3

__pencolor__ = QColor(30, 30, 30)
__lightBrush__ = QColor(89, 89, 89)
__darkBrush__ = QColor(72, 72, 72)

__lines__: typing.List[QLineF] = []
__lightRects__: typing.List[QRectF] = []
__darkRects__: typing.List[QRectF] = []


class Grid:
    @staticmethod
    def computeGrid(sceneRect: QRectF) -> None:
        __lines__.clear()
        __lightRects__.clear()
        __darkRects__.clear()

        tracks = [1, 3, 4, 1]

        left = int(sceneRect.left() - (sceneRect.left() % __pxPerFrame__)) + __xoffset__
        right = int(sceneRect.right())
        top = int(sceneRect.top() - sceneRect.top() % __trackHeight__) + __yoffset__
        bottom = int(sceneRect.bottom())

        start = top
        for nTracks in tracks:
            vSpacing = 0
            nSubTrack = 0
            totalTrackHeight = nTracks * __trackHeight__
            end = start + totalTrackHeight

            for y in range(start, end, __trackHeight__):
                vSpacing += __subTrackVSpacing__ if nSubTrack > 0 else 0
                dy = y + vSpacing

                for dx in range(left, right, __pxPerFrame__):
                    if nSubTrack % 2 == 0:
                        __darkRects__.append(
                            QRectF(dx, dy, __pxPerFrame__, __trackHeight__)
                        )
                    else:
                        __lightRects__.append(
                            QRectF(dx, dy, __pxPerFrame__, __trackHeight__)
                        )
                nSubTrack += 1

            start += (
                totalTrackHeight
                + __trackVSpacing__
                + (nTracks - 1) * __subTrackVSpacing__
            )

        # horizontal
        # for y in range(top, bottom + 1, __trackHeight__):
        #     __lines__.append(QLineF(0, y, right, y))

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
