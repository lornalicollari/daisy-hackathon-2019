from dataclasses import dataclass, field
from typing import List


@dataclass
class Car:
    acceleration_tier: int = 1
    braking_tier: int = 1
    top_speed_tier: int = 1
    gas_capacity_tier: int = 1
    tire_durability_tier: int = 1
    handling_tier: int = 1

    @property
    def acceleration(self) -> float:
        return [10, 15, 20, 25, 30][self.acceleration_tier - 1]

    @property
    def braking(self) -> float:
        return [10, 15, 20, 25, 30][self.braking_tier - 1]

    @property
    def top_speed(self) -> float:
        return [10, 20, 30, 40, 50][self.top_speed_tier - 1]

    @property
    def gas_capacity(self) -> float:
        return [500, 750, 1000, 1250, 1500][self.gas_capacity_tier - 1]

    @property
    def tire_durability(self) -> float:
        return [500, 750, 1000, 1250, 1500][self.tire_durability_tier - 1]

    @property
    def handling(self) -> int:
        return [9, 12, 15, 18, 21][self.handling_tier - 1]

    @property
    def cost(self) -> int:
        costs = [0, 2, 3, 4, 6]
        return costs[self.acceleration_tier - 1] + \
               costs[self.braking_tier - 1] + \
               costs[self.top_speed_tier - 1] + \
               costs[self.gas_capacity_tier - 1] + \
               costs[self.tire_durability_tier - 1] + \
               costs[self.handling_tier - 1]


@dataclass
class Point:
    i: int = None
    radius: float = None
    acceleration: float = None
    is_pit_stop: bool = None

    suggested_velocity: float = None
    max_velocity: float = None
    max_acceleration: float = None
    next = None

    gas_usage: float = None
    tire_wear: float = None

    prev: 'Point' = None
    next: 'Point' = None

    @property
    def velocity(self):
        return self.suggested_velocity if self.suggested_velocity is not None else self.max_velocity

    @velocity.setter
    def velocity(self, val: float):
        if self.suggested_velocity is not None:
            self.suggested_velocity = val
        else:
            self.max_velocity = val

    def __repr__(self):
        return f'Point {self.i}: radius={self.radius} acc={self.acceleration}/{self.max_acceleration} vel={self.max_velocity} pit_stop={self.is_pit_stop}'


@dataclass
class Track:
    points: List[Point] = field(default_factory=list)

    def get_radii(self) -> [float]:
        return list(map(lambda p: p.radius, self.points))
