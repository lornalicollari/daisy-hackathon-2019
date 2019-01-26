from reader import *
from models import *
from calculations import *
from itertools import tee
from typing import Iterable, TypeVar

T = TypeVar('T')


def pairwise(iterable: Iterable[T]) -> (T, T):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def fwd_pass(track: Track, car: Car):
    track.points[0].max_velocity = 0
    for prev, this in pairwise(track.points):
        this.max_velocity = min(prev.max_velocity + car.acceleration,
                                calc_max_velocity(this.radius, car.handling))


def bwd_pass(track: Track, car: Car):
    track.points[-1].max_acceleration = 0
    for next, this in pairwise(track.points[::-1]):
        this.max_acceleration = next.max_velocity - this.max_velocity
        if this.max_acceleration < -1 * car.breaking:
            this.max_acceleration = -1 * car.breaking
            this.max_velocity = next.max_velocity + car.breaking


if __name__ == '__main__':
    track = read_track_1()
