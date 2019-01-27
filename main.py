from processing import test, Car, read_track_n, Point
from writer import *

r, track = test(Car(), read_track_n(1))
print(r)
track.points = map(lambda p: Point(acceleration=p.max_acceleration, is_pit_stop=p.is_pit_stop),
                   track.points)
write_track_n(1, track)
write_car(Car())