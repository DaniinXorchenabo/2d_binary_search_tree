from abc import ABC
from typing import Generic, TypeVar

from python.try1.try6.structures._abstract_node import AbstractNode


AbstractNodeType = TypeVar("AbstractNodeType", bound=AbstractNode)


class ArcTreeIterator:
    def __init__(self, data: AbstractNodeType):
        self.data: AbstractNodeType | None = data

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
    def __init__(self, data: AbstractNodeType):
        self.left_item: AbstractNodeType | None = data

    def __iter__(self):
        return self

    def __next__(self):
        item = self.left_item
        self.left_item = self.left_item and self.left_item.next

        if item is None:
            raise StopIteration()
        return item


class AbstractTree(ABC,  Generic[AbstractNodeType]):
    def __init__(self):
        self.tree = None
        self.left_item: AbstractNodeType | None = None
        self.right_item: AbstractNodeType | None = None

    def add(self, new_item: AbstractNodeType):
        if self.tree is None:
            self.tree = new_item
            self.left_item = new_item
            self.right_item = new_item
        else:
            current_node: AbstractNodeType = self.tree
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

    def remove(self, rm_item: AbstractNodeType):
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
