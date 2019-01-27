import csv

from models import Track, Car


def write_track_n(n: int, track: Track):
    write_track(f'out/track_{n}.csv', track)


def write_track(file: str, track: Track):
    with open(file, 'w', newline='') as f:
        fieldnames = ['a', 'pit_stop']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        mapped_points = map(lambda p: {'a': p.acceleration, 'pit_stop': 1 if p.is_pit_stop else 0},
                            track.points)
        writer.writerows(mapped_points)


def write_car(car: Car):
    with open('out/car.csv', 'w', newline='') as f:
        fieldnames = ['acceleration', 'breaking', 'speed', 'gas', 'tire', 'handling']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        mapped_car = {'acceleration': car.acceleration_tier, 'breaking': car.braking_tier,
                      'speed': car.top_speed_tier, 'gas': car.gas_capacity_tier,
                      'tire': car.tire_durability_tier, 'handling': car.handling_tier}
        writer.writerow(mapped_car)
