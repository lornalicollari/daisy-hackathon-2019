from calculations import *
from models import *
from reader import *
from utils import pairwise, round_down, traverse


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
        if this.max_acceleration > car.acceleration:
            # Can't speed up enough, so correct next max velocity.
            this.max_acceleration = car.acceleration
            nxt.max_velocity = calc_velocity(this.max_velocity, this.max_acceleration)
            if nxt.next:
                calc(this.next, nxt.next)
        if this.max_acceleration < -1 * car.braking:
            # Can't slow down enough, so correct previous max velocity.
            this.max_acceleration = -1 * car.braking
            this.max_velocity = calc_velocity(nxt.max_velocity, car.braking)
        nxt.max_velocity = calc_velocity(this.max_velocity, this.max_acceleration)

    track.points[-1].max_acceleration = 0
    for second, first in pairwise(track.points[::-1]):
        calc(first, second)


def worthwhile_acceleration_pass(track: Track, car: Car):
    for this in track.points[1:-1]:
        nxt, lowest = find_next_lower(track, this)
        acceleration_cost = calc_cost(this.max_velocity, lowest.max_velocity,
                                      this.max_acceleration, this, nxt, car)
        acceleration_cost_2 = calc_cost(this.max_velocity, lowest.max_velocity / 2,
                                        this.max_acceleration / 2, this, nxt, car)
        # print(acceleration_cost, this.max_acceleration)
        if acceleration_cost <= 0 and this.max_velocity > 0 and this.max_acceleration > 0:
            this.max_acceleration = 0
            # print('not accel')
        if acceleration_cost_2 < acceleration_cost and this.max_velocity > 0 and this.max_acceleration > 0:
            this.max_acceleration /= 2
            nxt.max_velocity /= 2
            # print('half accel')
    for prev, nxt in pairwise(track.points):
        nxt.max_velocity = min(nxt.max_velocity, calc_velocity(prev.max_velocity, car.acceleration))


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
        if this.is_pit_stop:
            this.gas_usage = 0
            this.tire_wear = 0
            continue
        if this.gas_usage > car.gas_capacity:
            add_pit_stop(track, this.i)
            return False
        if this.tire_wear > car.tire_durability:
            add_pit_stop(track, this.i)
            return False
    return True


def add_pit_stop(track: Track, i: int):
    min_point = track.points[i - 1]
    # for point in track.points[i - 3:i - 10:-1]:
    #     if point.max_velocity < min_point.max_velocity:
    #         min_point = point
    min_point.is_pit_stop = True
    # print('pit at', min_point.i)


def find_next_lower(track: Track, this: Point) -> (Point, Point):
    lowest = this.next
    for point in traverse(this):
        if point.max_velocity <= this.max_velocity:
            return point, lowest
        if point.max_velocity < lowest.max_velocity:
            lowest = point
    return track.points[-1], lowest


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
    for a, b, s, g, t, h in [(a, b, s, g, t, h)
                             for a in trs for b in trs for s in trs for g in trs for t in trs for
                             h in trs]:
        cars.append(Car(a, b, s, g, t, h))
    return list(filter(lambda c: c.cost <= 18, cars))


def test(car: Car, track: Track, w: bool):
    max_velocity_pass(track, car)
    max_acceleration_pass(track, car)
    if w:
        worthwhile_acceleration_pass(track, car)
    done = False
    while not done:
        done = pit_stop_pass(track, car)
        max_velocity_pass(track, car)
        max_acceleration_pass(track, car)
        if w:
            worthwhile_acceleration_pass(track, car)
    return calc_points_time(track.points), track
