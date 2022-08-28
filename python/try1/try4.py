from typing import Optional

import pygame
from sortedcontainers import SortedKeyList
from binarytree import Node, NodeValue


class MyPoint(object):
    def __init__(self, x: float, y: float, color: tuple[int, int, int] = (255, 255, 255), radius: int = 10, real=True):
        self.x: float = x
        self.y: float = y
        self._color: tuple[int, int, int] = color
        self.r: int = radius
        self.real = real

    # def draw(self, screen_):
    #     pygame.draw.circle(screen_, self._color, self.center, self.r)
    #
    # def draw_w_and_h_lines(self, screen_, x_start_end=(0, WIDTH), y_start_end=(0, HEIGHT)):
    #     pygame.draw.aaline(screen_, self._color, (x_start_end[0], self.int_y), (x_start_end[1], self.int_y))
    #     pygame.draw.aaline(screen_, self._color, (self.int_x, y_start_end[0]), (self.int_x, y_start_end[1]))

    @property
    def int_x(self):
        return round(self.x)

    @property
    def int_y(self):
        return round(self.y)

    @property
    def center(self):
        return self.int_x, self.int_y

    @property
    def color(self):
        return tuple(
            [255 - i for i in self._color] if self._color[0] == self._color[1] == self._color[2] else self._color)

    @color.setter
    def color(self, new_color):
        self._color = tuple([255 - i for i in new_color] if new_color[0] == new_color[1] == new_color[2] else new_color)


class AbstractEvent(object):

    def __init__(self, point: MyPoint):
        self.is_deleted = False
        self.point = point


class SiteEvent(AbstractEvent):
    def __init__(self, point: MyPoint):
        super().__init__(point)


class CircleEvent(AbstractEvent):
    def __init__(self, point: MyPoint):
        super().__init__(point)


class AbstractNode(Node):
    def __init__(self,
                 value: NodeValue,
                 left: Optional["Node"] = None,
                 right: Optional["Node"] = None, ):
        super().__init__(value, left, right)


class ArcNode(AbstractNode):  # часть параболы
    def __init__(self,
                 f_point: MyPoint,
                 circle_event: Optional[CircleEvent] = None,
                 left: Optional["Node"] = None,
                 right: Optional["Node"] = None,
                 ):
        self.f_point = f_point
        self._circle_event = circle_event
        super().__init__(f_point.x, left, right)

    @property
    def circle_event(self):
        if self._circle_event is not None and self._circle_event.is_deleted is False:
            return self._circle_event
        else:
            self._circle_event = None
            return None

    @circle_event.setter
    def circle_event(self, value):
        if value is None and self._circle_event is not None:
            self._circle_event.is_deleted = True
        self._circle_event = value


class AbstractBreakPointNode(AbstractNode):
    def __init__(self,
                 value: MyPoint,
                 left: Optional[Node] = None,
                 right: Optional[Node] = None,
                 ):
        self.edge_graph = None  # ссылка на ребро графа
        self.event_point = value
        super().__init__(value.x, left, right)


class BreakPointNode(AbstractBreakPointNode):  # точка пересечения двух парабол
    def __init__(self,
                 start_point: NodeValue,
                 left: Optional[Node] = None,
                 right: Optional[Node] = None,

                 ):
        super().__init__(start_point, left, right)
        self._start_point = start_point
        self.dynamic_finish_point = start_point

    @property
    def start_point(self):
        return self._start_point


class RootSubtreeNode(AbstractBreakPointNode):
    def __init__(self,
                 value: NodeValue,
                 left: Optional[Node] = None,
                 right: Optional[Node] = None,

                 ):
        super().__init__(value, left, right)


def find_target_arc(event: AbstractEvent, sweep_line: Node) -> tuple[ArcNode, Optional[Node]]:
    parent = None
    while sweep_line is not ArcNode:
        assert sweep_line is not None, "где-то в коде допущена ошибка, дерево не должно уходить в None"
        if sweep_line.value < event.point.x:
            parent = sweep_line
            sweep_line = sweep_line.right
        else:
            parent = sweep_line
            sweep_line = sweep_line.left
    return sweep_line, parent


def site_process(event: AbstractEvent, sweep_line: Node):
    target_arc, target_arc_parent = find_target_arc(event, sweep_line)
    target_arc: ArcNode
    target_arc_parent: Optional[Node]
    target_arc.circle_event = None

    new_arc = ArcNode(event.point)
    new_node = RootSubtreeNode(
        event.point,
        left=BreakPointNode(
            event.point,
            left=target_arc,
            right=new_arc,
            ),
        right=BreakPointNode(
            event.point,
            left=new_arc,
            right=target_arc
        ),
    )

    if target_arc_parent is not None:
        if target_arc_parent.right == target_arc:
            target_arc_parent.right = new_node
        else:
            target_arc_parent.left = new_node
        return sweep_line
    else:
        return new_node


def circle_process(event: AbstractEvent):
    pass


def create_diagrams(points: list[MyPoint]):
    # points = sorted(points, key=lambda i: i.y)
    event_queue: SortedKeyList[AbstractEvent] = SortedKeyList([SiteEvent(i) for i in points], key=lambda e: e.point.y)
    sweep_line = RootSubtreeNode(ArcNode(None))
    while bool(event_queue):
        event: AbstractEvent = event_queue.pop(0)
        if event.is_deleted is False:
            if event is SiteEvent:
                sweep_line = site_process(event, sweep_line)
            else:
                circle_process(event)
        else:
            pass


from foronoi import Voronoi, Polygon, Visualizer, VoronoiObserver

# Define some points (a.k.a sites or cell points)
points = [
    (2.5, 2.5),
    (1, 7.5),
    (7.5, 2.5),
    (8, 7),
    (10, 6.5),
    (0.7, 6),
    (5, 5.5),
    (3, 3),
    (6, 3),
]

# Define a bounding box / polygon
polygon = Polygon([
    (2.5, 10),
    (5, 10),
    (10, 5),
    (10, 2.5),
    (5, 0),
    (2.5, 0),
    (0, 2.5),
    (0, 5),
])

# Initialize the algorithm
v = Voronoi(polygon)

# Attach a Voronoi Observer that monitors and visualizes the construction of
# the Voronoi Diagram step-by-step. See for more information
# examples/quickstart.py or examples/observers.py.
v.attach_observer(VoronoiObserver())

# Create the diagram
v.create_diagram(points=points)

# Get properties. See more examples in examples/quickstart.py
edges = v.edges
vertices = v.vertices
arcs = v.arcs
# points = v.points

# Plotting
# Note: plot_border_to_site() indicates with dashed line to which site a border
# belongs. The site's first edge is colored green.
Visualizer(v, canvas_offset=1)\
    .plot_sites(show_labels=True)\
    .plot_edges(show_labels=False)\
    .plot_vertices()\
    .plot_border_to_site()\
    .show()