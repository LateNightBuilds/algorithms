from typing import Callable

import numpy as np


class OneDimensionalGradientDescent:
    def __init__(self, num_iterations: int, step_size: float):
        self.num_iterations = num_iterations
        self.step_size = step_size

    def run(self, f_x: Callable, x_init: float):
        path = [x_init]
        for _ in range(self.num_iterations):
            x = path[-1]
            gradient = self._finite_difference(f_x=f_x, x=x)
            x_next = x - self.step_size * gradient
            path.append(x_next)

        return path

    @staticmethod
    def _finite_difference(f_x: Callable, x: float, delta: float = 1e-5):
        return (f_x(x + h) - f_x(x)) / delta


class OneDimensionalAdaptiveMovementEstimation:
    def __init__(self, num_iterations: int, alpha: float, first_moment_beta: float, second_moment_beta: float,
                 epsilon: float = 1e-5):
        self.num_iterations = num_iterations
        self.alpha = alpha
        self.first_moment_beta = first_moment_beta
        self.second_moment_beta = second_moment_beta
        self.epsilon = epsilon

    def run(self, f_x: Callable, x_init: float):
        path = [x_init]
        prev_first_movement = 0
        prev_second_movement = 0

        for _ in range(self.num_iterations):
            x = path[-1]
            gradient = self._finite_difference(f_x=f_x, x=x)
            first_moment = self._first_moment_estimation(prev_first_movement=prev_first_movement, gradient=gradient)
            second_moment = self._second_moment_estimation(prev_second_movement=prev_second_movement, gradient=gradient)
            x_next = x - self.alpha * first_moment / np.sqrt(second_moment + self.epsilon)

            prev_first_movement = first_moment
            prev_second_movement = second_moment
            path.append(x_next)

        return path

    @staticmethod
    def _finite_difference(f_x: Callable, x: float, delta: float = 1e-5):
        return (f_x(x + h) - f_x(x)) / delta

    def _first_moment_estimation(self, prev_first_moment: float, gradient: float):
        return self.first_moment_beta * prev_first_moment + (1 - self.first_moment_beta) * gradient

    def _second_moment_estimation(self, prev_second_moment: float, gradient: float):
        return self.second_moment_beta * prev_second_moment + (1 - self.second_moment_beta) * np.square(gradient)


def main():
    pass


if __name__ == '__main__':
    main()
