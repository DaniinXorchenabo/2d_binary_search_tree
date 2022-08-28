from abc import ABC
from decimal import Decimal


class AbstractPoint(ABC):
    def __init__(self, x:Decimal | int | float | None, y:Decimal | int | float | None):
        if isinstance(x, Decimal) is False and x is not None:
            x = Decimal(x)
        if isinstance(y, Decimal) is False and y is not None:
            y = Decimal(y)

        self.x: Decimal | None = x
        self.y: Decimal | None = y

    def __repr__(self):
        return f'({self.x}, {self.y})'

class Point(AbstractPoint):
    pass