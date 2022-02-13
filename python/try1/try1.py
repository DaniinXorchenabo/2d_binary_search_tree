from __future__ import annotations
import pygame
import random
from itertools import chain
from typing import Optional, Union, Any
from math import log

WIDTH = 700  # ширина игрового окна
HEIGHT = 700  # высота игрового окна
FPS = 30  # частота кадров в секунду

# lines = [[[10, 10], [10, 10]]]
# base1(5, 20)
# screen.fill((0, 0, 0))
# [pygame.draw.aaline(screen, (255, 255, 255),
#                     point1,
#                     point2) for (point1, point2) in lines]
list_tree: dict[int, Optional[MyPoint]] = dict()


class MyPoint(object):
    def __init__(self, x: float, y: float, color: tuple[int, int, int] = (255, 255, 255), radius: int = 10, real=True):
        self.x: float = x
        self.y: float = y
        self.color: tuple[int, int, int] = color
        self.r: int = radius
        self.real = real

    def draw(self, screen_):
        pygame.draw.circle(screen_, self.color, self.center, self.r)

    def draw_w_and_h_lines(self, screen_, x_start_end=(0, WIDTH), y_start_end=(0, HEIGHT)):
        pygame.draw.aaline(screen_, self.color, (x_start_end[0], self.int_y), (x_start_end[1], self.int_y))
        pygame.draw.aaline(screen_, self.color, (self.int_x, y_start_end[0]), (self.int_x, y_start_end[1]))

    @property
    def int_x(self):
        return round(self.x)

    @property
    def int_y(self):
        return round(self.y)

    @property
    def center(self):
        return self.int_x, self.int_y

    @classmethod
    def create_enter_point(cls, points_: list[MyPoint], color=(255, 0, 0), radius=10):
        return MyPoint(sum([i.x for i in points_]) / len(points_), sum([i.y for i in points_]) / len(points_),
                       color=color, radius=radius, real=False)

    @classmethod
    def division_4_groups(cls, center_point_: MyPoint, points_: list[MyPoint]):
        groups: list[list[MyPoint], list[MyPoint], list[MyPoint], list[MyPoint]] = [[], [], [], []]
        for p in points_:
            index: int = int(center_point_.x < p.x) + int(center_point_.y < p.y) * 2
            p.color = tuple([255 - 45 * index] * 3)
            groups[index].append(p)

        return groups

    @classmethod
    def draw_all(cls, screen_, points_: list[list[MyPoint, ...]]):
        [i.draw(screen_) for i in chain(points_)]

    @classmethod
    def create_binary_tree(
            cls, screen_, points_, deep=0, finding_map: dict[MyPoint, list[Optional[MyPoint]]] = dict(),
            last_center_point: Optional[tuple[MyPoint, int]] = None, yield_=False,
            x_start_end: tuple[int, int] = (0, WIDTH), y_start_end: tuple[int, int] = (0, HEIGHT)
    ):
        print(">>", points_)

        if len(points_) > 1:
            center_point = MyPoint.create_enter_point(points_, color=(255 - 45 * deep, 30 * deep % 255, 0))
            center_point.draw(screen_)
            center_point.draw_w_and_h_lines(screen_, x_start_end=x_start_end, y_start_end=y_start_end)
            if last_center_point is not None:
                finding_map[last_center_point[0]][last_center_point[1]] = center_point

            finding_map[center_point] = [None] * 4
            # MyPoint.draw_all(screen, points_)
            # if deep == 0 and yield_ is True:
            #     yield []
            if yield_ is True:
                MyPoint.draw_all(screen_, points_)
                # yield
            new_points = MyPoint.division_4_groups(center_point, points_)
            gens = [cls.create_binary_tree(screen_, i, deep=deep + 1, finding_map=finding_map,
                                           last_center_point=(center_point, ind), yield_=yield_,
                                           x_start_end=(x_start_end[0] + (
                                               0 if ind % 2 == 0 else abs(center_point.int_x - x_start_end[0])),
                                                        x_start_end[1] - (0 if ind % 2 == 1 else abs(
                                                            center_point.int_x - x_start_end[1]))),
                                           y_start_end=(y_start_end[0] + (
                                               0 if ind // 2 == 0 else abs(center_point.int_y - y_start_end[0])),
                                                        y_start_end[1] - (0 if ind // 2 == 1 else abs(
                                                            center_point.int_y - y_start_end[1]))),
                                           ) for ind, i in
                    enumerate(new_points)]
            if yield_ is True:
                yield gens
        elif bool(points_):
            if last_center_point is not None:
                finding_map[last_center_point[0]] = finding_map.get(last_center_point[0], [None] * 4)
                # print(last_center_point, finding_map.get(last_center_point[0], None), points_)
                finding_map[last_center_point[0]][last_center_point[1]] = points_[0]

        return finding_map

    @classmethod
    def create_binary_tree_as_list(
            cls, screen_, points_, deep=0
            , yield_=False,
            x_start_end: tuple[int, int] = (0, WIDTH), y_start_end: tuple[int, int] = (0, HEIGHT),
            parent_index: int = 0, number_group: int = 1
    ):
        global list_tree
        # print(">>", points_)

        if len(points_) > 1:
            center_point = MyPoint.create_enter_point(points_, color=(255 - 45 * deep, 30 * deep % 255, 0))
            center_point.draw(screen_)
            center_point.draw_w_and_h_lines(screen_, x_start_end=x_start_end, y_start_end=y_start_end)

            my_index = parent_index * 4 + number_group
            list_tree[my_index] = center_point

            if yield_ is True:
                MyPoint.draw_all(screen_, points_)

            new_points = MyPoint.division_4_groups(center_point, points_)
            gens = [cls.create_binary_tree_as_list(
                screen_, i, deep=deep + 1, yield_=yield_,
                x_start_end=(x_start_end[0] + (0 if ind % 2 == 0 else abs(center_point.int_x - x_start_end[0])),
                             x_start_end[1] - (0 if ind % 2 == 1 else abs(center_point.int_x - x_start_end[1]))),
                y_start_end=(y_start_end[0] + (0 if ind // 2 == 0 else abs(center_point.int_y - y_start_end[0])),
                             y_start_end[1] - (0 if ind // 2 == 1 else abs(center_point.int_y - y_start_end[1]))),
                parent_index=my_index,

                number_group=ind + 1

            ) for ind, i in enumerate(new_points)]

            if yield_ is True:
                res = yield gens
                # if isinstance(res, dict):
                #     list_tree |= res
        elif len(points_) == 1:
            my_index = parent_index * 4 + number_group
            list_tree[my_index] = points_[0]
        return list_tree

    @classmethod
    def find_point(cls, screen_, find_point_: MyPoint, points_map: dict[MyPoint, list[Optional[MyPoint]]],
                   start_point: Optional[MyPoint] = None):

        if start_point is None:
            start_point: MyPoint = list(points_map.keys())[0]
            last_start_color = start_point.color
            start_point.color = 0, 0, 255
            start_point.draw(screen_)
            start_point.color = last_start_color
            yield

        last_start_color = start_point.color
        start_point.color = 0, 0, 150
        start_point.draw(screen_)
        new_start_point = points_map[start_point][
            int(start_point.x < find_point_.x) + int(start_point.y < find_point_.y) * 2]

        print(new_start_point, new_start_point not in points_map,
              int(start_point.x < find_point_.x) + int(start_point.y < find_point_.y) * 2,
              start_point, points_map[start_point])
        if new_start_point is None or new_start_point not in points_map:
            new_start_point_color = (0, 255, 255)
            if new_start_point is not None:
                new_start_point_color = new_start_point.color
                new_start_point.color = 0, 255, 0
                new_start_point.r += 10
                new_start_point.draw(screen_)
                print('---------------------------------------------------------')

            yield
            if new_start_point is not None:
                new_start_point.color = 0, 0, 0
                new_start_point.draw(screen_)
                new_start_point.color = new_start_point_color
                new_start_point.r -= 10
                new_start_point.draw(screen_)
            start_point.color = last_start_color
            start_point.draw(screen_)

            yield

            return new_start_point
        else:
            new_start_point_color = new_start_point.color
            new_start_point.color = 0, 0, 255
            new_start_point.draw(screen_)
            new_start_point.color = new_start_point_color

            gen = cls.find_point(screen_, find_point_, points_map, new_start_point)
            yield gen

            start_point.color = last_start_color
            start_point.draw(screen_)
            # new_start_point.color = new_start_point.color[0], new_start_point.color[1], 255
            # new_start_point.draw(screen_)

            return gen

    @classmethod
    def find_point_in_tree(cls, screen_, find_point_: MyPoint, points_tree: list[Optional[MyPoint]], start_index: int):
        start_point: MyPoint = points_tree[start_index]

        if start_index == 0:
            last_start_color = start_point.color
            start_point.color = 0, 0, 255
            start_point.draw(screen_)
            start_point.color = last_start_color
            yield

        last_start_color = start_point.color
        start_point.color = 0, 0, 150
        start_point.draw(screen_)

        index = (int(start_point.x < find_point_.x) + int(start_point.y < find_point_.y) * 2) + 1 + (start_index * 4)

        print(start_index, index, int(start_point.x < find_point_.x) + int(start_point.y < find_point_.y) * 2 + 1,
              start_index * 4,
              (points_tree[index] if len(points_tree) > index else "----"), len(points_tree))

        # print(*['\t' * (((int(log(ind - (ind % 4 == 0), 4) + 1) + 1) if ind != 0 else 0) )+ str(i) + '\n' ])

        # last = 0
        # print(str(0).center(4) + str(points_tree[0]))
        # for ind, i in enumerate(points_tree[1:], 1):
        #     if ind != 1:
        #         t = int(log(ind - 1 - last * 4, 4))
        #         last = max(t, last)
        #
        #     print(str(ind).center(4) + '\t' * (last + 1) + str(i))

        new_start_point = None
        if len(points_tree) <= index or (new_start_point := points_tree[index]) is None:

            if len(points_tree) <= index or points_tree[index] is None:
                new_start_point = points_tree[start_index]
            else:
                new_start_point = points_tree[index]

            new_start_point_color = (0, 255, 255)
            if new_start_point is not None and new_start_point.real is True:
                new_start_point_color = new_start_point.color
                new_start_point.color = 0, 255, 0
                new_start_point.r += 10
                new_start_point.draw(screen_)
                print('---------------------------------------------------------')

            yield
            if new_start_point is not None:
                new_start_point.color = 0, 0, 0
                new_start_point.draw(screen_)
                new_start_point.color = new_start_point_color
                new_start_point.r -= 10
                new_start_point.draw(screen_)
            start_point.color = last_start_color
            start_point.draw(screen_)

            yield

            return new_start_point
        else:
            new_start_point = points_tree[index]
            new_start_point_color = new_start_point.color
            new_start_point.color = 0, 0, 255
            new_start_point.draw(screen_)
            new_start_point.color = new_start_point_color

            gen = cls.find_point_in_tree(screen_, find_point_, points_tree, index)
            yield gen

            start_point.color = last_start_color
            start_point.draw(screen_)
            # new_start_point.color = new_start_point.color[0], new_start_point.color[1], 255
            # new_start_point.draw(screen_)

            return gen

    def __repr__(self):
        return f'P({self.int_x}, {self.int_y}, {self.color[0] == self.color[1] == self.color[2]})'


def main2():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("My Game")
    clock = pygame.time.Clock()
    running = True
    lines = []
    points = [MyPoint(random.random() * (WIDTH - 20) + 10, random.random() * (HEIGHT - 20) + 10) for i in range(20)]
    [i.draw(screen) for i in points]

    # center_point = MyPoint.create_enter_point(points)
    # center_point.draw(screen)
    # center_point.draw_w_and_h_lines(screen)
    # new_points = MyPoint.division_4_groups(center_point, points)
    # MyPoint.draw_all(screen, new_points)
    # ------------------------------------------------------
    # finding_map_ = MyPoint.create_binary_tree(screen, points)
    # MyPoint.draw_all(screen, points)
    # print('-' * 20)
    # print(*finding_map_.items(), sep='\n')
    #
    # while running:
    #     for event in pygame.event.get():
    #         # проверить закрытие окна
    #         if event.type == pygame.QUIT:
    #             running = False
    #     pygame.display.flip()
    #     clock.tick(FPS)
    # ---------------------------------------------------------
    finding_map_ = dict()
    list_tree_as_dict = dict()
    generators = [MyPoint.create_binary_tree_as_list(screen, points, yield_=True, number_group=0)]
    # MyPoint.draw_all(screen, points)
    # print('-' * 20)
    # print(*finding_map_.items(), sep='\n')
    can_create_point = False
    find_generator = None
    last_find_generator = None
    tree_list = []

    while running:
        for event in pygame.event.get():
            # проверить закрытие окна
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:

                    def ddd():
                        global can_create_point
                        try:
                            if bool(generators):
                                generators.extend(next(generators[0]))
                            else:
                                can_create_point = True
                                print('end!!!!!!!!!!!!!!!!')
                        except StopIteration as e:
                            print('error is', e, [e], e.args)
                            if bool(generators):
                                generators.pop(0)
                                ddd()
                            else:
                                can_create_point = True
                                print('end!!!!!!!!!!!!!!!!')

                    ddd()
                if event.key == pygame.K_SPACE and can_create_point is True:  #
                    # print('K_SPACE')
                    if last_find_generator is not None:
                        try:
                            next(last_find_generator)
                        except StopIteration as e:
                            last_find_generator = None
                            print('err11', e.args, [e])
                    try:
                        new_gen = next(find_generator)
                        if new_gen is not None:
                            last_find_generator = find_generator
                            find_generator = new_gen
                        else:
                            pass
                            # last_find_generator = find_generator

                            # last_find_generator = None
                            # next(find_generator)
                    except StopIteration as e:
                        print('err', e.args, [e])

            if event.type == pygame.MOUSEBUTTONDOWN and can_create_point is True:
                pos = pygame.mouse.get_pos()
                find_point = MyPoint(*pos, color=(255, 255, 0))
                find_point.draw(screen)
                # find_generator = MyPoint.find_point(screen, find_point, finding_map_)

                last_find_generator = None
                # tree_list.append(list(finding_map_.keys())[0])
                # print(*list_tree.items(), sep = '\n')
                tree_list = []
                l_ = log(max(list_tree.keys()), 4)
                for i in range(sum([4 ** i for i in range(0, (int(l_) if l_ % 1 == 0 else (int(l_) + 1)) + 1)])):
                    tree_list.append(list_tree.get(i, None))
                print(len(tree_list))
                find_generator = MyPoint.find_point_in_tree(screen, find_point, tree_list, 0)

        pygame.display.flip()
        clock.tick(FPS)


def main1():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("My Game")
    clock = pygame.time.Clock()
    running = True
    lines = []
    points = [MyPoint(random.random() * (WIDTH - 20) + 10, random.random() * (HEIGHT - 20) + 10) for i in range(20)]
    [i.draw(screen) for i in points]

    center_point = MyPoint.create_enter_point(points)
    center_point.draw(screen)
    center_point.draw_w_and_h_lines(screen)
    new_points = MyPoint.division_4_groups(center_point, points)
    MyPoint.draw_all(screen, new_points)
    # ------------------------------------------------------
    finding_map_ = MyPoint.create_binary_tree(screen, points)
    MyPoint.draw_all(screen, points)
    print('-' * 20)
    print(*finding_map_.items(), sep='\n')

    while running:
        for event in pygame.event.get():
            # проверить закрытие окна
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
        clock.tick(FPS)


def get_index(deep: int, last_ind: int, last_group_number0: int, str_ind: int, x_classification: bool,
              y_classification: bool):
    _index = 4 ** deep + last_ind + (last_group_number0) + int(x_classification) + (4 * deep) * (str_ind // 2) + (
        2 ** (deep + 1) if y_classification is True else 0)
    _index = _index + _index % (4 ** deep)
    return _index


def get_base(deep):
    if deep == 0:
        return 1
    return 4 ** deep + get_base(deep - 1)


def get_index2(deep: int, last_x_index: int, last_y_index: int,
               x_classification: bool, y_classification: bool):
    # print(deep)
    return (get_base(deep) + last_x_index * 2 + int(x_classification) +
            (last_y_index * 2 + int(y_classification)) * 2 ** (deep + 1)
            )


def testing(last_m, next_m):
    next_m = [[j for j in i] for i in next_m]
    for i, coll in enumerate(last_m):
        for j, item in enumerate(coll):
            for x_pos in [False, True]:
                for y_pos in [False, True]:
                    next_m[i * 2 + int(y_pos)][j * 2 + int(x_pos)] = get_index(int(len(next_m) // 4), item,
                                                                               j % 2 + (i % 2 * 2), i * 2 + int(y_pos),
                                                                               x_pos, y_pos)
    print(*[', '.join(map(lambda i: str(i).center(4), i)) for i in next_m], "========", sep='\n')


def testing2(last_m, next_m):
    next_m = [[j for j in i] for i in next_m]
    for i, coll in enumerate(last_m):
        for j, item in enumerate(coll):
            for x_pos in [False, True]:
                for y_pos in [False, True]:
                    next_m[i * 2 + int(y_pos)][j * 2 + int(x_pos)] -= get_index2(int(log(len(next_m), 2)) - 1, j, i,
                                                                                 x_pos, y_pos)
    print(*[', '.join(map(lambda i: str(i).center(4), i)) for i in next_m], "========", sep='\n')


if __name__ == '__main__':
    main2()
    print(*[[0]], sep='\n')
    st, end = 1, 5
    last_arr = [[0]]
    for deep in range(1, 5):
        arr = [[i + j for j in range(2 ** (deep))] for i in range(st, end, 2 ** (deep))]
        testing2(last_arr, arr)
        print(*[', '.join(map(lambda i: str(i).center(4), i)) for i in arr], '---\n', sep='\n')
        st, end = end, end + 4 ** (deep + 1)
        last_arr = arr
    print(get_index(2, 29, 2, 4, False, False))
    print(get_index(1, 3, 2, 2, False, False))
    print(get_base(3))
