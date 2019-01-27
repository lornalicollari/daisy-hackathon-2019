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


def fwd_pass_1(track: Track, car: Car):
    track.points[0].max_velocity = 0
    for prev, this in pairwise(track.points):
        this.max_velocity = 0 if this.is_pit_stop else \
            min(car.top_speed,
                calc_velocity(prev.max_velocity, car.acceleration),
                calc_max_velocity(this.radius, car.handling))


def bwd_pass_1(track: Track, car: Car):
    track.points[-1].max_acceleration = 0
    for next, this in pairwise(track.points[::-1]):
        this.max_acceleration = min((next.max_velocity ** 2 - this.max_velocity ** 2) / 2,
                                    car.acceleration)
        if this.max_acceleration < -1 * car.breaking:
            this.max_acceleration = -1 * car.breaking
            next.max_velocity = calc_velocity(this.max_velocity, this.max_acceleration)


def fwd_pass_2(track: Track, car: Car):
    track.points[0].gas_usage = calc_gas_usage(track.points[0].max_acceleration)
    track.points[0].tire_wear = calc_tire_wear(track.points[0].max_acceleration)
    for prev, this in pairwise(track.points):
        this.gas_usage = prev.gas_usage + calc_gas_usage(this.max_acceleration)
        this.tire_wear = prev.tire_wear + calc_tire_wear(this.max_acceleration)
        if this.gas_usage > car.gas_capacity:
            # print('Gas!', this.i)
            add_pit_stop(track, this.i)
            return False
        if this.tire_wear > car.tire_duration:
            # print('Tires!', this.i)
            add_pit_stop(track, this.i)
            return False
        if this.is_pit_stop:
            this.gas_usage = 0
            this.tire_wear = 0
        # print(this)
    return True


def add_pit_stop(track: Track, i: int):
    min_point = track.points[i - 1]
    for point in track.points[i - 2:i - 10:-1]:
        if point.max_velocity < min_point.max_velocity:
            min_point = point
    # print(min_point)
    min_point.is_pit_stop = True
    # print(min_point)


def find_next_lower(track: Track, this_index: int):
    this = track.points[this_index]
    for i, nxt in enumerate(track.points[this_index + 1:]):
        if nxt.max_velocity <= this.max_velocity:
            return i, nxt


def find_optimal_car():
    r = []
    for car in build_cars():
        sum = 0
        for i in range(1, 9):
            sum += test(car, read_track_n(i))
        r.append((sum, car))
    print(sorted(r, key=lambda c: c[0]))


def build_cars():
    cars = []
    trs = range(5)
    acceleration = [10, 15, 20, 25, 30]
    breaking = [10, 15, 20, 25, 30]
    top_speed = [10, 20, 30, 40, 50]
    gas_capacity = [500, 750, 1000, 1250, 1500]
    tire_duration = [500, 750, 1000, 1250, 1500]
    handling = [9, 12, 15, 18, 21]
    cost = [0, 2, 3, 4, 6]
    for c in [(a, b, s, g, t, h)
              for a in trs for b in trs for s in trs for g in trs for t in trs for h in trs]:
        cars.append(Car(acceleration[c[0]], breaking[c[1]], top_speed[c[2]], gas_capacity[c[3]],
                        tire_duration[c[4]], handling[c[5]],
                        cost[c[0]] + cost[c[1]] + cost[c[2]] + cost[c[3]] + cost[c[4]] + cost[
                            c[5]]))
    return list(filter(lambda c: c.cost <= 18, cars))


def test(car: Car, track: Track):
    fwd_pass_1(track, car)
    bwd_pass_1(track, car)
    done = False
    while not done:
        done = fwd_pass_2(track, car)
        fwd_pass_1(track, car)
        bwd_pass_1(track, car)
    return calc_points_time(track.points)


if __name__ == '__main__':
    find_optimal_car()
