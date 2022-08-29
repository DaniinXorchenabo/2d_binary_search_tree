from __future__ import annotations

from dataclasses import dataclass
from typing import NamedTuple

from python.try1.try6.points._abstract_point import Point, AbstractPoint
from python.try1.try6.structures._abstract_tree import AbstractTree
from python.try1.try6.structures.arc_node import ArcNode


class ArcTree(AbstractTree[ArcNode]):

    def __repr__(self):
        m: list[list[ArcNode]] = []
        s: list[list[str]] = []
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
            l_arr = arr[:len(arr) // 2]
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
            for ind in range(len(arr) // 2, len(arr)):
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
                    next_arr.append((i.left, st - 5, st - 1))
                    # print(en + 1)
                    s[-1][st - 1] = '/'
                if i.right is not None:
                    next_arr.append((i.right, en + 1, en + 5))
                    # print(en + 1)
                    s[-1][en + 1] = '\\'

            arr = next_arr
            next_arr = []

        return '\n'.join([''.join(i) for i in s])


from random import randint

tree = ArcTree()

[tree.add(ArcNode(Point(x=0, y=randint(-10, 99)))) for i in range(100)]
arr = [i for i in tree]
print(tree)
print(arr)
for i in range(20):
    rm_index = randint(0, len(arr) - 1)
    rm_item = arr.pop(rm_index)
    print(
        f"iteration: {str(i).center(2)}, rm index: {str(rm_index).center(2)}, rm item is {rm_item}, len arr before: {len(list(tree))}",
        end=' ')
    tree.remove(rm_item)
    print(f'len arr after: {len(list(tree))}')
    print(tree)
print([i for i in tree])
