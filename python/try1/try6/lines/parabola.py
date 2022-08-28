from decimal import Decimal
from idlelib.debugobj import dispatch

from python.try1.try6.lines._abstract_line import AbstractLine
from python.try1.try6.lines.straight_line import StraightLine
from python.try1.try6.points._abstract_point import AbstractPoint, Point
from python.try1.try6.ranges._abstract_range import Range
from python.try1.try6.utils import normalize_class


class ParabolaLine(AbstractLine):

    # def __init__(self, a: Decimal, b: Decimal, c: Decimal):
    #     self.func = lambda x: a*x*x + b*x + c

    # def __init__(self, p:Decimal, x1: Decimal,y1:Decimal):
    #
    #     def _f(x):
    #         try:
    #             res = Decimal((2*p*(x - x1))**0.5)
    #             return [-(res - y1), (res-y1)]
    #         except Exception as e:
    #             return None
    #
    #     self.y_func = _f

    def __init__(self, p:Decimal, focus: AbstractPoint):
        p = Decimal(p)
        self.p = Decimal(p)
        self.focus = focus

        def _f(x):
            try:

                # xd = focus.x + p
                # x = (y - focus.y)**2/(focus.x - xd) + (focus.x + xd)/2

                if x == focus.x + p / 2:
                    return focus.y
                r = -2*p*(x - (focus.x + p/2))
                # print(r)
                res = Decimal(float(r)**0.5)
                return [-res + focus.y, +res+focus.y]
            except Exception as e:
                # print(e)
                return None

        self.y_func = _f
        if p != 0:
            self.x_func = lambda y: ( (y - focus.y)**2/(-2 * p) + (focus.x + p/2))
        else:
            self.x_func = lambda y: Range(low=float("-inf"), high=focus.x)

    def __and__(self, other: AbstractLine) -> AbstractPoint | list[AbstractPoint] | AbstractLine | None:
        if isinstance(other, StraightLine):
            if other.is_horizontal:
                _y = -other.C/other.B
                return normalize_class(x=self.x_func(_y), y=_y)
            elif other.is_vertical:
                _x = -other.C/other.A
                _ys = self.y_func(_x)
                points = [Point(x=_x, y=i) for i in (_ys if isinstance(_ys, list) else [_ys]) if i is not None]
                if bool(points):
                    return points
                return None
            else:
                raise ValueError("Пересечение между произвольной прямой линией и параболой пока что не поддерживаются")

        elif isinstance(other, ParabolaLine):
            if other.p == 0 or self.p == 0:
                if other.p == 0 and self.p == 0:
                    return (Range(low=float('-inf'), high=min(other.focus.x, self.focus.x))
                            if other.focus.y == self.focus.y else None)
                this, other = (self, other) if self.p == 0 else (other, self)
                return normalize_class(x=other.x_func(this.focus.y), y=this.focus.y)

            else:
                raise ValueError("Пересечения между двумя произвольными параболами пока что не поддерживаются")

    def __rand__(self, other):
        pass

    def __repr__(self):
        return f'(y - {self.focus.y})^2 = -2 * {self.p} * (x - ({self.focus.x} - {self.p} / 2))'


line1 = StraightLine(0, 1, -9)
line2 = StraightLine(0, 1, 3)
line3 = StraightLine(1,0, -1)
line4 = StraightLine(1, 0, -4)
line5 = StraightLine(1,0, -6)

arc1 = ParabolaLine(6, Point(x=1, y=3))
print(arc1.y_func(4))
print(arc1.x_func(3))
print(arc1 & line1)
print(arc1 & line2)
print(arc1 & line3)
print(arc1 & line4)
print(arc1 & line5)
