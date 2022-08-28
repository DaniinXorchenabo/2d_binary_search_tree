from __future__ import annotations
from dataclasses import dataclass
from collections import namedtuple
import enum

from python.try1.try5.VoronoiDiagram import Site, HalfEdge


@dataclass
class Face:  # ячейка
    site: Site
    outerComponent: HalfEdge


@dataclass
class Event:
    ...


@dataclass
class Arc:
    class Color(enum.Enum):
        RED = 'red'
        BLACK = 'black'

    parent: Arc
    left: Arc
    right: Arc

    site: Site
    leftHalfEdge: HalfEdge  # указывает на полуребро, отрисованное крайней левой точкой дуги
    rightHalfEdge: HalfEdge  #  — на полуребро, отрисованное крайней правой точкой
    event: Event

    prev:Arc  # используются для получения прямого доступа к предыдущей и следующей дуге береговой линии
    next: Arc  # используются для получения прямого доступа к предыдущей и следующей дуге береговой линии

    color: Color
