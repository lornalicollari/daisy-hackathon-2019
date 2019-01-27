import csv

from models import Track


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
