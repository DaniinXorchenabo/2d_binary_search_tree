from __future__ import annotations
from abc import ABC, abstractmethod

from python.try1.try6.points._abstract_point import AbstractPoint
from python.try1.try6.ranges._abstract_range import AbstractRange


class AbstractLine(ABC):
    @abstractmethod
    def __and__(self, right: AbstractLine) -> AbstractPoint | AbstractLine | None:
        pass

    @abstractmethod
    def __rand__(self, left: AbstractLine) -> AbstractPoint | AbstractLine | None:
        pass
