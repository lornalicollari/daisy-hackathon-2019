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
    i: int
    radius: float
    acceleration: float = None
    is_pit_stop: bool = None

    max_velocity: float = None
    max_acceleration: float = None

    gas_usage: float = None
    tire_wear: float = None


@dataclass
class Track:
    points: List[Point] = field(default_factory=list)

    def get_radii(self) -> [float]:
        return list(map(lambda p: p.radius, self.points))
