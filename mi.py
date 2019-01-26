import numpy as np
from scipy.optimize import minimize
from reader import *
import matplotlib.pyplot as plt


# def func(inputs: List[int]) -> int:
#     track = read_track_n(1)
#     for point in track.points:
#         point.acceleration =
#         inputs[0] *

def calc_time(distance: int, velocity: int, acceleration: int) -> float:
    acceleration_time = velocity / acceleration
    acceleration_distance = 0.5 * velocity * acceleration_time
    remaining_distance = distance - acceleration_distance
    remaining_time = remaining_distance / velocity
    if remaining_distance < 0: raise Exception
    return acceleration_time + remaining_time


distance = 200
velocity = 35
capacity = 500
accelerations = np.arange(5, velocity + 1)
costs = list(
    map(lambda a: (0.1 * a ** 2) / capacity * 30 + calc_time(distance, velocity, a), accelerations))
print(costs)
times = list(map(lambda a: calc_time(distance, velocity, a), accelerations))

plt.plot(accelerations, costs)
plt.show()
