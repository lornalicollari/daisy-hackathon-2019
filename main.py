from processing import test, Car, read_track_n, Point
from writer import *
from itertools import product
from joblib import Parallel, delayed
from tqdm import tqdm
import multiprocessing

multipliers = {1: 1, 2: 0.25, 3: 0.25, 4: 0.25, 5: 0.5, 6: 0.5, 7: 1, 8: 1}


def build_cars():
    cars = []
    for comb in product(range(1, 5 + 1), repeat=6):
        car = Car(comb[0], comb[1], comb[2], comb[3], comb[4], comb[5])
        if car.cost <= 18:
            cars.append(car)
    return cars

results = []


def test_car(car):
    total_score = 0
    for track_num in range(1, 8 + 1):
        time, track = test(car, read_track_n(track_num))
        if len(results) > 0 and total_score > min(results, key=lambda r: r[0])[0]:
            # print('\n', total_score, 'stopped on track', track_num)
            return None
        track.points = map(
            lambda p: Point(acceleration=p.max_acceleration, is_pit_stop=p.is_pit_stop),
            track.points)
        total_score += multipliers[track_num] * time

    results.append((total_score, car))
    return total_score


def test_cars():
    results_p = []
    cpu_count = multiprocessing.cpu_count()
    try:
        results_p = Parallel(n_jobs=cpu_count, require='sharedmem')(
            delayed(test_car)(car) for car in tqdm(build_cars()))
    except Exception:
        pass

    # for i, car in enumerate(build_cars()):
    #     total_score = test_car(car, results)
    #     if total_score:
    #         print(i, total_score, car)

    print('\n\n\n')
    print(list(sorted(results, key=lambda r: r[0])))
    print('\n\n\n')
    print(list(sorted(results_p, key=lambda r: r[0])))


if __name__ == '__main__':
    car = Car(gas_capacity_tier=5, tire_durability_tier=5, handling_tier=5)
    score = test_car(car)
    print(score)
