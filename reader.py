from models import Track, Point
import csv


def read_track_n(n: int):
    return read_track(f'res/track_{n}.csv')


def read_track(file: str) -> Track:
    track = Track()
    i = 0
    with open(file) as f:
        for row in csv.DictReader(f):
            track.points.append(Point(i, float(row['radius'])))
            i += 1
    return track
