__width__ = 10
__height__ = 20


def alignToGrid(value: float) -> float:
    return round(value / __width__) * __width__
