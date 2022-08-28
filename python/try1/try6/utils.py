from decimal import Decimal

from python.try1.try6.lines.straight_line import RangeLine
from python.try1.try6.points._abstract_point import Point
from python.try1.try6.ranges._abstract_range import Range


def normalize_class(
        x: Decimal | int | float | Range | None =None,
        y: Decimal | int | float | Range | None =None
):
    if isinstance(x, Range) and isinstance(y, Range):
        raise ValueError('области из двух отрезков пока что не поддерживаются')
    if isinstance(x, (float, int)):
        x = Decimal(x)
    if isinstance(y, (float, int)):
        y = Decimal(y)
    if isinstance(x, Range) or isinstance(y, Range):
        return RangeLine(x=x, y=y)
    return Point(x=x, y=y)