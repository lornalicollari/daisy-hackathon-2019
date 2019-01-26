from math import *


def calc_velocity(velocity: int, acceleration: int):
    """
    Calculates the velocity when the car travels from point x to point x+1.

    :param velocity: Velocity at point x.
    :param acceleration: Acceleration at point x.
    :return: Velocity at point x+1.
    """
    radicand = (velocity ** 2) + (2 * acceleration)
    return sqrt(radicand)


def calc_travel_time(velocity: int, acceleration: int = 0):
    """
    Calculates the time it takes to travel from point x to point x+1.

    :param velocity: Velocity at point x.
    :param acceleration: Acceleration at point x.
    :return: Time to travel between point x and point x+1.
    """
    if acceleration == 0:
        return 1 / velocity  # distance = 1 m
    else:
        return (calc_velocity(velocity, acceleration) - velocity) / acceleration


def calc_max_velocity(radius: int, handling: int):
    """
    Calculates the maximum velocity of car with given handling coefficient
    at point with given radius of curvature.

    :param radius: Radius of curvature at the point.
    :param handling: Handling coefficient of the car.
    :return: Maximum velocity of the car at the point.
    """
    radicand = (radius * handling) / 1_000_000
    return sqrt(radicand)


def calc_gas_usage(acceleration: int):
    """
    Calculates how much gas is consumed when breaking.

    :param acceleration: Acceleration at the point.
    :return: Gas usage at the point.
    """
    if acceleration > 0:
        return 0.1 * (acceleration ** 2)
    else:
        return 0


def calc_wear(acceleration: int):
    """
    Calculates how much wear has been done to the tire while breaking (de-accelerating)
    :param acceleration: Acceleration at the point.
    :return: Tire wear at the point.
    """
    if acceleration < 0:
        return 0.1 * (acceleration ** 2)
    else:
        return 0
