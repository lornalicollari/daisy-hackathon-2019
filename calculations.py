from math import *
from models import *
from typing import List

STRAIGHT_LINE = -1
INFINITY = 1_000_000


def calc_velocity(velocity: float, acceleration: float):
    """
    Calculates the velocity when the car travels from point x to point x+1.

    :param velocity: Velocity at point x.
    :param acceleration: Acceleration at point x.
    :return: Velocity at point x+1.
    """
    radicand = (velocity ** 2) + (2 * acceleration)
    if radicand < 0:
        return 0
    else:
        return sqrt(radicand)


def calc_travel_time(velocity: float, acceleration: float = 0, distance: float = 1):
    """
    Calculates the time it takes to travel from point x to point x+1.

    :param velocity: Velocity at point x.
    :param acceleration: Acceleration at point x.
    :param distance: Number of points of travel.
    :return: Time to travel between point x and point x+distance.
    """
    if velocity == 0:
        return 0
    elif acceleration == 0:
        return distance / velocity  # distance = 1 m
    elif distance == 1:
        return (calc_velocity(velocity, acceleration) - velocity) / acceleration
    else:
        acceleration_time = calc_travel_time(velocity, acceleration)
        acceleration_distance = (velocity * acceleration_time) + \
                                (0.5 * acceleration * acceleration_time ** 2)
        remaining_distance = distance - acceleration_distance
        if remaining_distance < 0:
            raise Exception
        remaining_time = calc_travel_time(velocity, distance=remaining_distance)
        return acceleration_time + remaining_time


def calc_max_velocity(radius: float, handling: int):
    """
    Calculates the maximum velocity of car with given handling coefficient
    at point with given radius of curvature.

    :param radius: Radius of curvature at the point. STRAIGHT_LINE if straight line.
    :param handling: Handling coefficient of the car.
    :return: Maximum velocity of the car at the point. INFINITY if no max.
    """
    if radius == STRAIGHT_LINE:
        return INFINITY
    else:
        radicand = (radius * handling) / 1_000_000
        return sqrt(radicand)


def calc_gas_usage(acceleration: float):
    """
    Calculates how much gas is consumed when breaking.

    :param acceleration: Acceleration at the point.
    :return: Gas usage at the point.
    """
    if acceleration > 0:
        return 0.1 * (acceleration ** 2)
    else:
        return 0


def calc_tire_wear(acceleration: float):
    """
    Calculates how much wear has been done to the tire while breaking (de-accelerating)
    :param acceleration: Acceleration at the point.
    :return: Tire wear at the point.
    """
    if acceleration < 0:
        return 0.1 * (acceleration ** 2)
    else:
        return 0


# def calc_travel_time(points: List[Point], initial_velocity: int = 0):
#     velocity = initial_velocity
#     time = 0
#     for point in points:
#         time += calc_travel_time(velocity, point.acceleration)
#         velocity = calc_velocity(velocity, point.acceleration)
#     return time


def calc_cost(acceleration: float, start_point: Point, end_point: Point, car: Car):
    wear = calc_tire_wear(acceleration)
    gas = calc_gas_usage(acceleration)

    return 30 * 0.5 * (wear / car.tire_durability + gas / car.gas_capacity) - time_gained


def calc_points_time(points: List[Point], initial_velocity: int = 0):
    velocity = initial_velocity
    time = 0
    for point in points:
        time += calc_travel_time(velocity, point.max_acceleration)
        velocity = calc_velocity(velocity, point.max_acceleration)
        if point.is_pit_stop:
            time += 30
    return time

# def calc_travel_time(points: List[Point], initial_velocity: int = 0):
#     velocity = initial_velocity
#     time = 0
#     for point in points:
#         time += calc_travel_time(velocity, point.acceleration)
#         velocity = calc_velocity(velocity, point.acceleration)
#     return time
