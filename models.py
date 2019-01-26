from dataclasses import dataclass, field


@dataclass
class Car:
    acceleration: int
    breaking: int
    top_speed: int
    gas_capacity: int
    tire_duration: int
    handling: int


@dataclass
class Point:
    radius: float
    acceleration: float = None
    is_pit_stop: bool = None


@dataclass
class Track:
    points: [Point] = field(default_factory=list)

    def get_radii(self) -> [float]:
        return list(map(lambda p: p.radius, self.points))
