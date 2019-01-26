from dataclasses import dataclass


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
    radius: int
    acceleration: int
    is_pit_stop: bool


@dataclass
class Track:
    points: [Point]
