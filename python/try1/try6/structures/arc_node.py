from __future__ import annotations

from dataclasses import dataclass
from typing import NamedTuple

from python.try1.try6.points._abstract_point import Point, AbstractPoint
from python.try1.try6.structures._abstract_node import AbstractNode


class ArcNode(AbstractNode):

    def __init__(self, focus: Point, parent=None, left=None, right=None):
        super().__init__(parent=parent, left=left, right=right)
        self.focus: Point = focus

    @staticmethod
    def _gel_value(value: ArcNode | AbstractPoint):
        if value is None:
            return None
        if isinstance(value, ArcNode):
            value = value.focus
        return value.y

    def __repr__(self):
        return f'{self.__class__.__name__}[{self.focus.x}, {self.focus.y}]'
