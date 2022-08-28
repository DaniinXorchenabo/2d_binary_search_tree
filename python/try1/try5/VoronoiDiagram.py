from __future__ import annotations
from dataclasses import dataclass
from collections import namedtuple
import enum

PointType = namedtuple("PointType", ['x', 'y'])


@dataclass
class Site:
    index: int
    point: PointType
    face: Face


@dataclass
class Vertex:
    point: PointType


@dataclass
class HalfEdge:
    origin: Vertex
    destination: Vertex
    twin: HalfEdge
    incidentFace: Face
    prev: HalfEdge
    next: HalfEdge