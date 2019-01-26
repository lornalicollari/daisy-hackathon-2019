from models import *
import csv


def read_track_n(n: int):
    return read_track(f'res/track_{n}.csv')


def read_track(file: str) -> Track:
    track = Track()
    with open(file) as f:
        for row in csv.DictReader(f):
            track.points.append(Point(float(row['radius'])))
    return track
