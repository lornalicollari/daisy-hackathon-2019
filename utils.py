from itertools import tee
from typing import TypeVar, Iterable

T = TypeVar('T')


def pairwise(iterable: Iterable[T]) -> (T, T):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
