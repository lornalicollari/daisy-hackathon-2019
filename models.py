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
        return [10, 15, 20, 25, 30][self.acceleration_tier]

    @property
    def braking(self) -> float:
        return [10, 15, 20, 25, 30][self.braking_tier]

    @property
    def top_speed(self) -> float:
        return [10, 20, 30, 40, 50][self.top_speed_tier]

    @property
    def gas_capacity(self) -> float:
        return [500, 750, 1000, 1250, 1500][self.gas_capacity_tier]

    @property
    def tire_durability(self) -> float:
        return [500, 750, 1000, 1250, 1500][self.tire_durability_tier]

    @property
    def handling(self) -> float:
        return [9, 12, 15, 18, 21][self.handling_tier]

    @property
    def cost(self) -> int:
        costs = [0, 2, 3, 4, 6]
        return costs[self.acceleration_tier] + \
               costs[self.braking_tier] + \
               costs[self.top_speed_tier] + \
               costs[self.gas_capacity_tier] + \
               costs[self.tire_durability_tier] + \
               costs[self.handling_tier]


@dataclass
class Point:
    i: int = None
    radius: float = None
    acceleration: float = None
    is_pit_stop: bool = None

    max_velocity: float = None
    max_acceleration: float = None

    gas_usage: float = None
    tire_wear: float = None

    prev: 'Point' = None
    next: 'Point' = None


@dataclass
class Track:
    points: List[Point] = field(default_factory=list)

    def get_radii(self) -> [float]:
        return list(map(lambda p: p.radius, self.points))
