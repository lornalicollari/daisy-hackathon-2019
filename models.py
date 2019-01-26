from dataclasses import dataclass, field
from typing import List


@dataclass
class Car:
    acceleration: int = 10
    breaking: int = 10
    top_speed: int = 10
    gas_capacity: int = 500
    tire_duration: int = 500
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
