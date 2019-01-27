from models import Track, Point
import csv


def read_track_n(n: int):
    return read_track(f'res/track_{n}.csv')


def read_track(file: str) -> Track:
    track = Track()
    with open(file) as f:
        for i, row in enumerate(csv.DictReader(f)):
            point = Point(i, float(row['radius']), prev=track.points[-1])
            point.prev.next = point
            track.points.append(point)
    return track
