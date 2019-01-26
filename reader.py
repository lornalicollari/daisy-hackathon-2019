from models import *
import csv


def read_track_1():
    return read_track('res/track_1.csv')


def read_track(file: str) -> Track:
    track = Track()
    with open(file) as f:
        for row in csv.DictReader(f):
            track.points.append(Point(row['radius']))
    return track
