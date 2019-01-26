import matplotlib.pyplot as plt
import numpy
from reader import *
from calculations import *

H = 9


def plot_track_n_radii(n: int):
    track_1 = read_track_n(n)

    distances = numpy.arange(len(track_1.points))

    plt.plot(distances, track_1.get_radii())
    plt.title(f'Track {n} Radii')
    plt.show()


def plot_track_n_velocities(n: int):
    track_n = read_track_n(n)
    distances = numpy.arange(len(track_n.points))
    max_velocities = []

    for radius in track_n.get_radii():
        max_v = calc_max_velocity(radius, H)
        max_v = 10 if max_v == -1 else max_v
        max_velocities += [min(10, max_v)]

    plt.plot(distances, max_velocities)
    plt.title(f'Track {n} Max Velocities')
    plt.show()


if __name__ == '__main__':
    for n in range(1, 9):
        plot_track_n_radii(n)
        plot_track_n_velocities(n)
