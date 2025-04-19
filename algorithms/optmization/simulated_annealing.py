import random
from dataclasses import dataclass
from itertools import pairwise
from typing import List, Tuple

import numpy as np


@dataclass
class Point:
    x: float
    y: float

    def euclidean_distance(self, other_point: 'Point') -> float:
        return np.sqrt((self.x - other_point.x) ** 2 + (self.y - other_point.y) ** 2)


@dataclass
class Route:
    points: List[Point]

    def get_total_distance(self):
        return sum(curr_point.euclidean_distance(other_point=next_point)
                   for curr_point, next_point in pairwise(self.points))

    def to_edges_list(self) -> List[Tuple[Point, Point]]:
        return [(curr_point, next_point)
                for curr_point, next_point in pairwise(self.points)]


class SimulatedAnnealingTSP:
    def __init__(self, points: List[Point],
                 initial_temp: float = 1000, cooling_rate: float = 0.99,
                 stop_temp: float = 1e-4, max_iter: int = 100000):

        self.current_route = Route(points=points)
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.stop_temp = stop_temp
        self.max_iter = max_iter

    def run_simulated_annealing_travel_salesman_problem(self) -> List[Tuple[Point, Point]]:
        current_route = self.current_route
        best_route = self.current_route
        best_distance = best_route.get_total_distance()
        temp = self.initial_temp

        for _ in range(self.max_iter):
            if temp < self.stop_temp:
                break

            new_route: Route = self._suggest_new_route(current_route=current_route)
            if self._should_explore_new_route(current_route=current_route, new_route=new_route, temp=temp):
                current_route = new_route
                new_route_distance = new_route.get_total_distance()
                if new_route_distance < best_distance:
                    best_distance = new_route_distance
                    best_route = new_route

            temp *= self.cooling_rate

        return best_route.to_edges_list()

    @staticmethod
    def _should_explore_new_route(new_route: Route, current_route: Route, temp: float) -> bool:
        current_distance = current_route.get_total_distance()
        new_distance = new_route.get_total_distance()

        if new_distance < current_distance:
            return True

        acceptance_prob = np.exp((current_distance - new_distance) / temp)
        if acceptance_prob > random.random():
            return True

        return False

    @staticmethod
    def _suggest_new_route(current_route: Route) -> Route:
        new_points = current_route.points.copy()
        i, j = random.sample(range(len(new_points)), 2)
        new_points[i], new_points[j] = new_points[j], new_points[i]
        return Route(points=new_points)


if __name__ == "__main__":
    np.random.seed(42)
    random_points = [Point(x=p[0], y=p[1]) for p in np.random.rand(10, 2) * 100]

    simulated_annealing = SimulatedAnnealingTSP(points=random_points)
    edge_list = simulated_annealing.run_simulated_annealing_travel_salesman_problem()

    for edge in edge_list:
        print(edge)
