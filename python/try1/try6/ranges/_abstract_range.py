from __future__ import annotations
from abc import ABC
from decimal import Decimal
from typing import Literal


class AbstractRange(ABC):
    def __init__(self, low: Decimal | float | None, high: Decimal | float | None):
        if low in [float('inf'), float('-inf'), None]:
            low = low or float('-inf')
        elif isinstance(low, Decimal) is False:
            low = Decimal(low)
        if high in [float('inf'), float('-inf'), None]:
            high = high or float('inf')
        elif isinstance(high, Decimal) is False:
            high = Decimal(low)

        self.low: Decimal | Literal[float('inf')] | Literal[float('-inf')] = low
        self.high:  Decimal | Literal[float('inf')] | Literal[float('-inf')] = high

    def __contains__(self, x:  Decimal | float | int):
        return self.low <= x <= self.high

    def __repr__(self):
        return f'(from: {self.low}  to: {self.high})'

    def __and__(self, other : int | float | Decimal | AbstractRange):
        if isinstance(other, (int , float)):
            other = Decimal(other)
        if isinstance(other, Decimal):
            return (other if self.low <= other <= self.high else None)
        elif isinstance(other, AbstractRange):
            low = (self.low or other.low) and max(self.low or float('-inf'), other.low or float('-inf'))
            high = (self.high or other.high) and min(self.high or float('inf'), other.high or float('inf'))
            return self.__class__(low=low, high=high)
        raise ValueError(f'Тип {type(other)} пока не поддерживает операцию & с AbstractRange')

    def __rand__(self, other):
        return self.__and__(other)


class Range(AbstractRange):
    pass
