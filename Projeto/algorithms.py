from collections import deque
from city import distance, GeoCity, Euc_2D, GeoCoord
from tspparse import read_tsp_file
import numpy as np
import random
import math
from copy import deepcopy, copy
import matplotlib.pyplot as plt
from pprint import pprint
from tqdm import tqdm


def calc_distance(tsp, city1_index, city2_index):
    """Calculate distance between cities by their (one-based) indices"""
    cities = tsp["CITIES"]
    return distance(cities[city1_index - 1], cities[city2_index - 1])


def path_length(tsp, path):
    """Find the length of a path of cities given as a list"""
    if len(path) == 1:
        return 0
    else:
        start_node = path.pop()
        next_node = path[-1]
        return calc_distance(tsp, start_node, next_node) + path_length(tsp, path)


def tour_from_path(path):
    """Append the first city in a path to the end in order to obtain a tour"""
    path.append(path[0])
    return path


def in_order_path(tsp):
    """Return the tour [1,2,...,n,1] where n is the dimension of the TSP"""
    dim = tsp["DIMENSION"]
    return list(range(1, dim + 1))


def in_order_tour(tsp):
    """Return the tour obtained by traveling to each city in order and circling around back to the first city"""
    return tour_from_path(in_order_path(tsp))


def calc_in_order_tour(tsp):
    """Calculate the distance of the in-order-tour for a tsp"""
    return path_length(tsp, in_order_tour(tsp))


def nearest_neighbor(tsp, untraveled_cities, current_city):
    """Given a set of city keys, find the key corresponding to the closest city"""
    distance_to_current_city = lambda city: calc_distance(tsp, current_city, city)
    return min(untraveled_cities, key=distance_to_current_city)


def furthest_neighbor(tsp, untraveled_cities, current_city):
    """Given a set of city keys, find the key corresponding to the closest city"""
    distance_to_current_city = lambda city: calc_distance(tsp, current_city, city)
    return max(untraveled_cities, key=distance_to_current_city)


def nearest_neighbor_tour(tsp):
    """Construct a tour through all cities in a TSP by following the nearest neighbor heuristic"""
    nearest_neighbor_path = [1]
    current_city = 1
    cities_to_travel = set(range(2, tsp["DIMENSION"] + 1))

    while cities_to_travel:
        current_city = nearest_neighbor(tsp, cities_to_travel, current_city)
        nearest_neighbor_path.append(current_city)
        cities_to_travel.remove(current_city)

    return tour_from_path(nearest_neighbor_path)


def furthest_neighbor_tour(tsp):
    """Construct a tour through all cities in a TSP by following the furthest neighbor heuristic"""
    nearest_neighbor_path = [1]
    current_city = 1
    cities_to_travel = set(range(2, tsp["DIMENSION"] + 1))

    while cities_to_travel:
        current_city = furthest_neighbor(tsp, cities_to_travel, current_city)
        nearest_neighbor_path.append(current_city)
        cities_to_travel.remove(current_city)

    return tour_from_path(nearest_neighbor_path)


def calc_nearest_neighbor_tour(tsp):
    return path_length(tsp, nearest_neighbor_tour(tsp))


def calc_furthest_neighbor_tour(tsp):
    return path_length(tsp, furthest_neighbor_tour(tsp))


def linear_rate(T0, alpha):
    T = T0 = 10**T0
    temps = []
    t = 0
    while round(T, 6) > 0.0:
        T = T0 - (alpha * t)
        temps.append(T)
        # print(T)
        t += 1
    # exit(0)
    return temps


def exp_rate(T0, alpha):
    T = T0 = 10**T0
    temps = []
    t = 0
    while round(T, 6) > 0.0:
        T = T0 * (alpha**t)
        temps.append(T)
        t += 1
    return temps


def e_power(arg):
    try:
        ans = math.exp(arg)
    except OverflowError:
        ans = float('inf')
    return ans


def tour_length(tsp, tour):
    return path_length(tsp, deepcopy(tour))


INVERSE_SECTION = 'INVERSE_SECTION'
INVERSE_PAIR = 'INVERSE_PAIR'


def _generate_random_neighbor(tsp, tour, method=INVERSE_SECTION):
    tour = tour[0]
    [i, j] = sorted(random.sample(range(1, tsp["DIMENSION"]), 2))
    if method == INVERSE_SECTION:
        newTour = tour[:i] + copy(tour[i:j + 1])[::-1] + tour[j + 1:]
    else:
        newTour = tour[:i] + tour[j:j + 1] + tour[i + 1:j] + tour[i:i + 1] + tour[j + 1:]
    assert len(tour) == len(newTour)
    # assert len(set(tour)) == len(tour) - 1
    # assert len(set(newTour)) == len(newTour) - 1
    # assert set(tour) == set(newTour)
    return newTour, tour_length(tsp, newTour)


def _generate_tour_at_0(tsp):
    tour = random.sample(range(tsp["DIMENSION"]), tsp["DIMENSION"])
    idx0 = tour.index(0)
    aux = tour[0]
    tour[0] = tour[idx0]
    tour[idx0] = aux
    tour.append(0)
    return tour, tour_length(tsp, tour)


from datetime import datetime


def sa(tsp, T0=5, N=1, alpha=0.5, rate_func=linear_rate, verbose=True):
    inicio = datetime.now()

    best_tour = current_tour = _generate_tour_at_0(tsp)

    agenda_temp = rate_func(T0=T0, alpha=alpha)

    if verbose:
        print("T0=10^{} N={} alpha={} rate={}".format(T0, N, alpha, rate_func))
        bar = tqdm(agenda_temp)
    else:
        bar = agenda_temp

    for temperature in bar:
        # print(temperature)
        for i in range(N):
            new_tour = _generate_random_neighbor(tsp, current_tour)

            if e_power((current_tour[1] - new_tour[1]) / temperature) > random.uniform(0.0, 1.0):
                current_tour = deepcopy(new_tour)
                if best_tour[1] > current_tour[1]:
                    best_tour = deepcopy(current_tour)

                if verbose:
                    bar.set_description("Best= {} / New= {}".format(best_tour[1], current_tour[1]))
                    bar.refresh()

        # if best_tour[1] == 6859:
        #     break

    tempo_total = str((datetime.now() - inicio))
    return best_tour, tempo_total, dict(tsp=tsp, T0=T0, N=N, alpha=alpha)
