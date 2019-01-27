from calculations import *
from models import *
from reader import *
from utils import pairwise


def max_velocity_pass(track: Track, car: Car):
    """
    Calculates the maximum velocity in one forward pass.
    """

    def calc(prev: Point, this: Point):
        this.max_velocity = 0 if this.is_pit_stop \
            else min(car.top_speed,
                     calc_velocity(prev.max_velocity, car.acceleration),
                     calc_max_velocity(this.radius, car.handling),
                     calc_max_velocity(prev.radius, car.handling))

    track.points[0].max_velocity = 0
    for first, second in pairwise(track.points):
        # Find maximum possible velocities at each point.
        calc(first, second)


def max_acceleration_pass(track: Track, car: Car):
    """
    Calculates the maximum acceleration (and corrects maximum velocity if necessary) in
    one backwards pass.
    """

    def calc(this: Point, nxt: Point):
        # Find maximum acceleration.
        this.max_acceleration = (nxt.max_velocity ** 2 - this.max_velocity ** 2) / 2
        this.max_acceleration = min(car.acceleration, this.max_acceleration)
        this.max_acceleration = max(-1 * car.breaking, this.max_acceleration)
        # Correct maximum acceleration
        new_nxt_max_velocity = calc_velocity(this.max_velocity, this.max_acceleration)
        if new_nxt_max_velocity != nxt.max_velocity:
            nxt.max_velocity = new_nxt_max_velocity
            calc(this.prev, nxt.prev)

    track.points[-1].max_acceleration = 0
    for second, first in pairwise(track.points[::-1]):
        calc(first, second)


def pit_stop_pass(track: Track, car: Car):
    """
    Looks for first point where gas or tires run out in one forward pass,
    and add a pit stop at or slightly before it.
    """
    track.points[0].gas_usage = calc_gas_usage(track.points[0].max_acceleration)
    track.points[0].tire_wear = calc_tire_wear(track.points[0].max_acceleration)
    for prev, this in pairwise(track.points):
        this.gas_usage = prev.gas_usage + calc_gas_usage(this.max_acceleration)
        this.tire_wear = prev.tire_wear + calc_tire_wear(this.max_acceleration)
        if this.gas_usage > car.gas_capacity:
            add_pit_stop(track, this.i)
            return False
        if this.tire_wear > car.tire_duration:
            add_pit_stop(track, this.i)
            return False
        if this.is_pit_stop:
            this.gas_usage = 0
            this.tire_wear = 0
    return True


def add_pit_stop(track: Track, i: int):
    min_point = track.points[i - 1]
    for point in track.points[i - 2:i - 10:-1]:
        if point.max_velocity < min_point.max_velocity:
            min_point = point
    min_point.is_pit_stop = True


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
    max_velocity_pass(track, car)
    max_acceleration_pass(track, car)
    done = False
    while not done:
        done = pit_stop_pass(track, car)
        max_velocity_pass(track, car)
        max_acceleration_pass(track, car)
    return calc_points_time(track.points), track
