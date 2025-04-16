from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Tuple, List

import matplotlib.pyplot as plt
import numpy as np
import sklearn
from sklearn.datasets import make_classification, make_moons
from sklearn.inspection import DecisionBoundaryDisplay
from sklearn.preprocessing import StandardScaler


@dataclass
class Point:
    x: float
    y: float


def run_multilayer_perceptron(X: List[Point], y: int, alpha: float):
    multilayer_perceptron = sklearn.neural_network.MLPClassifier(hidden_layer_sizes=(64, 64),
                                                                 alpha=alpha, random_state=42)
    multilayer_perceptron.fit(X=X, y=y)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    x_min, x_max = X_scaled[:, 0].min() - 0.5, X_scaled[:, 0].max() + 0.5
    y_min, y_max = X_scaled[:, 1].min() - 0.5, X_scaled[:, 1].max() + 0.5
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 300), np.linspace(y_min, y_max, 300))
    Z = multilayer_perceptron.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    return Z


def main():
    X, y = make_moons(n_samples=500, noise=0.3, random_state=42)

    alphas = [0, 0.01, 0.1, 1, 10]
    for alpha in alphas:
        run_multilayer_perceptron(X=X, y=y, alpha=alpha)

    plt.show()


if __name__ == '__main__':
    main()
