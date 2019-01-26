from dataclasses import dataclass, field
from typing import List

@dataclass
class Car:
    acceleration: float = 10
    breaking: float = 10
    top_speed: float = 10
    gas_capacity: float = 500
    tire_duration: float = 500
    handling: int = 9
    cost: int = 0


@dataclass
class Point:
    radius: float
    acceleration: float = None
    is_pit_stop: bool = None

    max_velocity: float = None
    max_acceleration: float = None


@dataclass
class Track:
    points: List[Point] = field(default_factory=list)

    def get_radii(self) -> [float]:
        return list(map(lambda p: p.radius, self.points))

    # def calc_time(self) -> float:
    #     return sum(calc_travel_time(p.max_velocity, p.max_acceleration) for p in self.points)
