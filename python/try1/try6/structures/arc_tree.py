from __future__ import annotations

from dataclasses import dataclass
from typing import NamedTuple

from python.try1.try6.points._abstract_point import Point, AbstractPoint


class ArcTreeIterator:
    def __init__(self, data: ArcNode):
        self.data: ArcNode | None = data

    def __iter__(self):
        return self

    def __next__(self):
        item = self.data
        if item.right is not None:
            self.data = self.data.right
            while True:
                if self.data.left is not None:
                    self.data = self.data.left
                elif self.data.right is not None:
                    self.data = self.data.right
                else:
                    break
        elif item.parent is not None:
            self.data = self.data.parent
        else:
            self.data = None

        if item is None:
            raise StopIteration()
        return item


class ArcTreeOptimizeIterator:
    def __init__(self, data: ArcNode):
        self.left_item: ArcNode | None = data

    def __iter__(self):
        return self

    def __next__(self):
        item = self.left_item
        self.left_item = self.left_item and self.left_item.next

        if item is None:
            raise StopIteration()
        return item


class ArcTree(object):

    def __init__(self):
        self.tree = None
        self.left_item = None
        self.right_item = None

    def add(self, new_item: ArcNode):
        if self.tree is None:
            self.tree = new_item
            self.left_item = new_item
            self.right_item = new_item
        else:
            current_node: ArcNode = self.tree
            while True:
                if current_node > new_item:
                    if current_node.left is None:
                        current_node.left = new_item
                        # new_item.parent = current_node

                        from_item = new_item.parent.prev
                        to_item = new_item.parent

                        new_item.prev = from_item
                        # if from_item is not None:
                        #     from_item.next = new_item
                        new_item.next = to_item
                        # if to_item is not None:
                        #     to_item.prev = new_item
                        break
                    else:
                        current_node = current_node.left
                else:
                    if current_node.right is None:
                        current_node.right = new_item
                        # new_item.parent = current_node

                        from_item = new_item.parent
                        to_item = new_item.parent.next

                        new_item.prev = from_item
                        # if from_item is not None:
                        #     from_item.next = new_item
                        new_item.next = to_item
                        # if to_item is not None:
                        #     to_item.prev = new_item

                        break
                    else:
                        current_node = current_node.right

            if new_item.prev is None:
                self.left_item = new_item
            if new_item.next is None:
                self.right_item = new_item

        return new_item

    def remove(self, rm_item: ArcNode):
        from_item = rm_item.prev
        to_item = rm_item.next



        if rm_item.left is not None and rm_item.right is not None:
            new_root_item, _, *_ = sorted(
                [i for i in [from_item, to_item] if i is not None],
                key=lambda i: abs(i.focus.y - rm_item.focus.y)
            ) + [None, None]
            if new_root_item is None:
                self.tree = None
                return
            if new_root_item.parent != rm_item:
                if new_root_item.left is not None:
                    last_child = new_root_item.left
                elif new_root_item.right is not None:
                    last_child = new_root_item.right
                else:
                    last_child = None

                if new_root_item.parent is None:
                    # self.tree = new_root_item
                    raise ValueError("")
                else:
                    if new_root_item.parent > new_root_item:
                        new_root_item.parent.left = last_child
                    else:
                        new_root_item.parent.right = last_child

                new_root_item.parent = rm_item.parent

                if new_root_item.parent is None:
                    self.tree = new_root_item

                new_root_item.left = rm_item.left
                new_root_item.right = rm_item.right

            else:
                if new_root_item.left is None and rm_item.left != new_root_item:
                    new_root_item.left = rm_item.left
                if new_root_item.right is None and rm_item.right != new_root_item:
                    new_root_item.right = rm_item.right

                new_root_item.parent = rm_item.parent
                if new_root_item.parent is None:
                    self.tree = new_root_item

            if new_root_item.prev is None:
                self.left_item = new_root_item
            if new_root_item.next is None:
                self.right_item = new_root_item
        elif rm_item.left is not None and rm_item.right is  None:
            new_root_item = rm_item.left
            new_root_item.parent = rm_item.parent
            if new_root_item.parent is None:
                self.tree = new_root_item
            if new_root_item.prev is None:
                self.left_item = new_root_item
            if new_root_item.next is None:
                self.right_item = new_root_item

        elif rm_item.left is  None and rm_item.right is not None:
            new_root_item = rm_item.right
            new_root_item.parent = rm_item.parent
            if new_root_item.parent is None:
                self.tree = new_root_item

            if new_root_item.prev is None:
                self.left_item = new_root_item
            if new_root_item.next is None:
                self.right_item = new_root_item
        #
        #     if new_child_item is not None:
        #         new_child_item.parent = new_root_item
        #     elif new_root_item is not None:
        #         if new_root_item.left in [None, rm_item]:
        #             new_root_item.left = new_child_item
        #         else:
        #             new_root_item.right = new_child_item
        #     if rm_item == self.tree:
        #         self.tree = new_root_item
        else:
            rm_item.parent = None
        #
        if from_item is not None:
            from_item.next = to_item
        elif to_item is not None:
            to_item.prev = from_item
        if from_item is None:
            self.left_item = to_item
        if to_item is  None:
            self.right_item = from_item



        rm_item.delete()
        a = 1


    def find_left(self):
        # current_node: ArcNode = self.tree
        # while True:
        #     if current_node.left is None:
        #         if current_node.right is None:
        #             break
        #         else:
        #             current_node = current_node.right
        #     else:
        #         current_node = current_node.left
        # return current_node
        return self.left_item

    def __iter__(self):
        return ArcTreeOptimizeIterator(self.find_left())

    def __repr__(self):
        m: list[list[ArcNode]] = []
        s :list[list[str]]= []
        arr: list[tuple[ArcNode, int, int]] = [(self.tree, 0, 4)]
        next_arr: list[tuple[ArcNode, int, int]] = []
        str_len = 1
        count = 0
        while bool(arr):
            count += 1
            if count > 100:
                break
            s.append([" "] * str_len)
            s.append([" "] * str_len)
            # print(arr, len(s[0]))
            l_arr =arr[:len(arr)//2]
            g_delta = 0
            for ind in range(len(l_arr) - 1, -1, -1):
                [i, st, en] = arr[ind]
                last_i, last_st, last_en = arr[ind + 1]
                if en + g_delta < last_st:
                    pass
                else:
                    delta = (en + g_delta) - last_st + 1
                    arr[ind] = i, st - delta, en - delta
                    g_delta = delta
            g_delta = 0
            for ind in range(len(arr)//2, len(arr)):
                [i, st, en] = arr[ind]
                last_i, last_st, last_en = arr[ind - 1]
                if (last_en + g_delta) < st:
                    pass
                else:
                    delta = (last_en + g_delta) - st + 1
                    arr[ind] = i, st + delta, en + delta
                    g_delta = delta
            delta = 0
            if arr[0][1] < 0:
                delta = 0 - arr[0][1] + 10
                for ind in range(len(arr)):
                    arr[ind] = arr[ind][0], arr[ind][1] + delta, arr[ind][2] + delta
            end_delta = arr[-1][2] - len(s[0]) - delta
            if end_delta < -3:
                end_delta = 0
            else:
                end_delta += 15
            if delta != 0 or end_delta != 0:
                if delta == 0:
                    delta = 15
                if end_delta == 0:
                    end_delta = 15
                for ind in range(len(s)):
                    s[ind] = ([' '] * delta) + s[ind] + ([' '] * end_delta)
                str_len = len(s[0])


            for [i, st, en] in arr:
                # while s[-2][st:en + 1]
                s[-2][st:en + 1] = list(str(i.focus.y).center(4, '.'))

                if i.left is not None:
                    next_arr.append((i.left,st-5,st-1 ))
                    # print(en + 1)
                    s[-1][st-1] = '/'
                if i.right is not None:
                    next_arr.append((i.right, en + 1, en + 5))
                    # print(en + 1)
                    s[-1][en + 1] = '\\'

            arr = next_arr
            next_arr = []

        return '\n'.join([''.join(i) for i in s])

    # def __repr__(self):
    #
    #     @dataclass
    #     class R:
    #         node: ArcNode
    #         parent: R | CH | None
    #         coll: int
    #         st: int
    #         end: int
    #
    #     @dataclass
    #     class CH:
    #         char: str
    #         parent: R | CH
    #         coll: int
    #         st: int
    #         end: int
    #
    #     _d : dict[ArcNode | None: R] = {
    #         self.tree: R(self.tree, None, 0, 0, 4),
    #         None: R(self.tree, None,0, 0, 4)
    #     }
    #
    #     arr: list[R] = [_d[self.tree]]
    #     next_arr: list[ArcNode] = []
    #     coll_count = -1
    #     while bool(arr):
    #         coll_count += 1
    #         for i in arr:
    #
    #             if i.node.left is not None:
    #                 data = R(i.node.left, coll_count, i.st)
    #                 next_arr.append(data)
    #                 _d[i] = R(i, coll_count, _d[i.parent])
    #             if i.node.right is not None:
    #                 next_arr.append(i.node.right)
    #                 _d[i] = R(i, coll_count, _d[i.parent])





class ArcNode(object):

    def __init__(self, focus: Point, parent=None, left=None, right=None):
        self._left: ArcNode | None = left
        self._right: ArcNode | None = right
        self._parent: ArcNode | None = parent
        self.focus: Point = focus
        self._prev: ArcNode | None = None
        self._next: ArcNode | None = None

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, value: ArcNode | None):
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
    def right(self, value: ArcNode | None):
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
    def parent(self, new_parent: ArcNode | None):
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
        if self._parent is not None :
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
    def prev(self, value: ArcNode | None):
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
    def next(self, value: ArcNode | None):
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
    def _gel_value(value: ArcNode | AbstractPoint):
        if value is None:
            return None
        if isinstance(value, ArcNode):
            value = value.focus
        return value.y

    def __lt__(self, other: ArcNode):
        return self._gel_value(self) < self._gel_value(other)

    def __le__(self, other: ArcNode):
        return self._gel_value(self) <= self._gel_value(other)

    # def __eq__(self, other: ArcNode):
    #     return self._gel_value(self) == self._gel_value(other)
    #
    # def __ne__(self, other: ArcNode):
    #     return self._gel_value(self) != self._gel_value(other)

    def __gt__(self, other: ArcNode):
        return self._gel_value(self) > self._gel_value(other)

    def __ge__(self, other: ArcNode):
        return self._gel_value(self) >= self._gel_value(other)

    def __repr__(self):
        return f'{self.__class__.__name__}[{self.focus.x}, {self.focus.y}]'

    def __del__(self):
        self.delete()

from random import randint

tree = ArcTree()

[tree.add(ArcNode(Point(x=0, y=randint(-10, 99)))) for i in range(100)]
arr = [i for i in tree]
print(tree)
print(arr)
for i in range(20):

    rm_index = randint(0, len(arr) - 1)
    rm_item = arr.pop(rm_index)
    print(f"iteration: {str(i).center(2)}, rm index: {str(rm_index).center(2)}, rm item is {rm_item}, len arr before: {len(list(tree))}", end=' ')
    tree.remove( rm_item)
    print(f'len arr after: {len(list(tree))}')
    print(tree)
print([i for i in tree])