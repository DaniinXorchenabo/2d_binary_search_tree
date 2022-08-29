from __future__ import annotations

from dataclasses import dataclass
from typing import NamedTuple

from python.try1.try6.points._abstract_point import AbstractPoint
from python.try1.try6.structures._abstract_node import AbstractNode
from python.try1.try6.structures.arc_node import ArcNode


class QueueNode(AbstractNode):

    def __init__(self, arc_node: ArcNode, parent=None, left=None, right=None):
        super().__init__(parent=parent, left=left, right=right)
        self.arc_node: ArcNode = arc_node

    @staticmethod
    def _gel_value(value: QueueNode | ArcNode | AbstractPoint):
        if value is None:
            return None
        if isinstance(value, QueueNode):
            value = value.arc_node
        if isinstance(value, ArcNode):
            value = value.focus
        return value.y

    def __repr__(self):
        return f'{self.__class__.__name__}[{self.arc_node.focus.x}, {self.arc_node.focus.y}]'
