import sys
from typing import Union

from models import Point
from dataclasses import dataclass
from calculations import *
from reader import *
from processing import *

@dataclass
class Tree:
    min_time: int = 2000


@dataclass
class Node:
    p: Point
    acceleration: float
    time: float
    velocity: float
    children: [] = field(default_factory=list)


def f(p: Point, a: float, t: float, v: float, parent: Node, depth, tree: Tree) -> Union[Node, None]:
    if not p:
        if parent.time < tree.min_time:
            tree.min_time = parent.time
            print(parent)
        return None
    # print(p)
    if v > 10:
        return
    min_a = (0 - v ** 2) / 2
    if a <= min_a:
        return
    if t > 1000.0 * depth / float(1000) or t > tree.min_time:
        # print(depth)
        return
    n = Node(p, a, t + calc_travel_time(v, a), v)
    for i in reversed(range(11)):
        next_a = 2 * i - 10
        n.children.append(f(p.next, next_a, t + calc_travel_time(v, a), calc_velocity(v, a), n, depth + 1, tree))
    return n


if __name__ == '__main__':
    track = read_track_n(5)
    fwd_pass(track, Car())
    bwd_pass(track, Car())
    sys.setrecursionlimit(1500)
    f(track.points[0], track.points[0].max_acceleration, 0, 0, None, 0, Tree())
