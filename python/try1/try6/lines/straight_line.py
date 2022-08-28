from decimal import Decimal
from idlelib.debugobj import dispatch

from python.try1.try6.lines._abstract_line import AbstractLine
from python.try1.try6.points._abstract_point import Point, AbstractPoint
from python.try1.try6.ranges._abstract_range import Range


class StraightLine(AbstractLine):

    # @dispatch(Decimal, Decimal)
    # @dispatch(int, int)
    # @dispatch(float, float)
    # def __init__(self, k: Decimal, b: Decimal):
    #     self.func = lambda x: k * x + b

    def __init__(self, A: Decimal | float | int, B: Decimal | float | int, C: Decimal | float | int):
        self.is_vertical = B == 0
        self.is_horizontal = A == 0
        self.A: Decimal = Decimal(A)
        self.B: Decimal = Decimal(B)
        self.C: Decimal = Decimal(C)
        self.y_func = lambda x: -(A / B) * x - (C / B)
        self.x_func = lambda y: -(B / A) * y - (C / A)
        if B == 0:
            self.y_func = lambda x: (Range(low=float('-inf'), high=float('inf')) if x * A == -C else None)
        elif A == 0:
            self.x_func = lambda y: (Range(low=float('-inf'), high=float('inf')) if y * B == -C else None)

    def __and__(self, other: AbstractLine):
        if isinstance(other, StraightLine) and isinstance(other, RangeLine) is False:
            A1, B1, C1 = self.A, self.B, self.C
            A2, B2, C2 = other.A, other.B, other.C
            if A1 == 0:
                A1, B1, C1, A2, B2, C2 = A2, B2, C2, A1, B1, C1
            if A1 == 0:
                return RangeLine(x=Range(low=float("-inf"), high=float("inf")), y=-C1 / B1) if (
                            C1 / B1 == C2 / B2) else None
            mn = A2 / A1
            B2 = (B1 * mn - B2)
            if B2 == 0:
                return RangeLine(x=-C1 / A1, y=Range(low=float("-inf"), high=float("inf"))) if (
                            C1 / A1 == C2 / A2) else None
            C2 = (C1 * mn - C2)
            mn = B1 / B2
            C1 = (C2 * mn - C1)
            return Point(x=C1 / A1, y=-C2 / B2)
        else:
            return other.__rand__(self)

    def __rand__(self, other):
        return self.__and__(other)


class RangeLine(StraightLine):

    def __init__(self, x: Decimal | int | float | Range, y: Decimal | int | float | Range):
        self.x_param = x
        self.y_param = y
        if isinstance(x, Range) and isinstance(y, Range):
            raise ValueError("Линия не может задаваться двумя отрезками")
        elif isinstance(x, Range):
            super().__init__(0, 1, -y)
            self.y_func = lambda x_: (self.y_func(x_) if x.low <= x_ <= x.high else None)
            self.x_func = lambda y_: (x if y_ * self.B == -self.C else None)
        elif isinstance(y, Range):
            super().__init__(1, 0, -x)
            self.x_func = lambda y_: (self.y_func(y_) if y.low <= y_ <= y.high else None)
            self.y_func = lambda x_: (y if x_ * self.A == -self.C else None)
        else:
            raise ValueError("Линия не может быть точкой")

    def __and__(self, other):
        if isinstance(other, RangeLine):
            res = other
        else:
            res = super().__and__(other)
        if isinstance(res, AbstractPoint):
            return self.y_func(res.x) and self.x_func(res.y) and res
        if isinstance(res, RangeLine):
            if (res.is_vertical == self.is_vertical):
                if self.is_vertical is True:
                    return RangeLine(x=self.x_param, y=self.y_param & res.y_param)
                else:
                    return RangeLine(x=self.x_param & res.x_param, y=self.y_param)
            else:
                if self.is_vertical is True:
                    return Point(x=res.x_param & self.x_param , y=self.y_param & res.y_param)
                else:
                    return Point(x=self.x_param & res.x_param, y=res.y_param & self.y_param )

# d = StraightLine(0, 1, 2)
# f = StraightLine(0, -2, -4)
# print(d & f)
