from __future__ import annotations
from abc import ABC, abstractstaticmethod, abstractmethod

from typing import Any


class AbstractNode(ABC):
    def __init__(self,  parent=None, left=None, right=None):
        self._left: AbstractNode | None = left
        self._right: AbstractNode | None = right
        self._parent: AbstractNode | None = parent
        self._prev: AbstractNode | None = None
        self._next: AbstractNode | None = None

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, value: AbstractNode | None):
        if value is not None:
            self._left = value
            del value.parent
            value._parent = self
        else:
            del self.left

    @left.deleter
    def left(self):
        if self._left is not None and self._left._parent == self:
            self._left._parent = None
        self._left = None

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, value: AbstractNode | None):
        if value is not None:
            self._right = value
            del value.parent
            value._parent = self
        else:
            del self.right

    @right.deleter
    def right(self):
        if self._right is not None and self._right._parent == self:
            self._right._parent = None
        self._right = None

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, new_parent: AbstractNode | None):
        if new_parent is not None:
            self._parent = new_parent
            if new_parent > self:
                del new_parent.left
                new_parent._left = self
            else:
                del new_parent.right
                new_parent._right = self

        else:
            del self.parent

    @parent.deleter
    def parent(self):
        if self._parent is not None:
            if self._parent > self:
                if self._parent._left == self:
                    self._parent._left = None
            else:
                if self._parent._right == self:
                    self._parent._right = None
        self._parent = None

    @property
    def prev(self):
        return self._prev

    @prev.setter
    def prev(self, value: AbstractNode | None):
        if value is not None:
            self._prev = value
            del value.next
            value._next = self
        else:
            del self.prev

    @prev.deleter
    def prev(self):
        if self._prev is not None and self._prev._next == self:
            self._prev._next = None
        self._prev = None

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, value: AbstractNode | None):
        if value is not None:
            self._next = value
            del value.prev
            value._prev = self
        else:
            del self.next

    @next.deleter
    def next(self):
        if self._next is not None and self._next._prev == self:
            self._next._prev = None
        self._next = None

    def delete(self):
        del self.parent
        del self.left
        del self.right
        del self.prev
        del self.next

    @staticmethod
    @abstractstaticmethod
    def _gel_value(value: AbstractNode | Any):
        pass

    def __lt__(self, other: AbstractNode):
        return self._gel_value(self) < self._gel_value(other)

    def __le__(self, other: AbstractNode):
        return self._gel_value(self) <= self._gel_value(other)

    # def __eq__(self, other: ArcNode):
    #     return self._gel_value(self) == self._gel_value(other)
    #
    # def __ne__(self, other: ArcNode):
    #     return self._gel_value(self) != self._gel_value(other)

    def __gt__(self, other: AbstractNode):
        return self._gel_value(self) > self._gel_value(other)

    def __ge__(self, other: AbstractNode):
        return self._gel_value(self) >= self._gel_value(other)

    @abstractmethod
    def __repr__(self):
        pass

    def __del__(self):
        self.delete()
