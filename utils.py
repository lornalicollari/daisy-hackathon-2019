import math
from itertools import tee
from typing import TypeVar, Iterable

from models import Point

T = TypeVar('T')


def pairwise(iterable: Iterable[T]) -> (T, T):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def traverse(point: Point):
    while point.next:
        point = point.next
        yield point


def round_down(num: float, digits: int) -> float:
    return 0.0 if num == 0 \
        else math.floor(abs(num) * (10 ** digits)) / float(10 ** digits) * (num / abs(num))
