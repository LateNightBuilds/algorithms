import numpy as np
import sklearn
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score
from sklearn.preprocessing import StandardScaler


class MLPClassifierForRegularizationImpact():
    def __init__(self, X, y, regularization):
        self.scaler = StandardScaler()
        self.X = self.scaler.fit_transform(X)
        self.y = y
        self.regularization = regularization
        self.model = sklearn.neural_network.MLPClassifier(hidden_layer_sizes=(16, 16),
                                                          alpha=self.regularization,
                                                          max_iter=2000,
                                                          random_state=42)

    def fit(self):
        self.model.fit(X=self.X, y=self.y)

    def predict(self):
        return self.model.predict(self.X)

    def get_decision_boundary(self):
        x_min, x_max = self.X[:, 0].min() - 0.5, self.X[:, 0].max() + 0.5
        y_min, y_max = self.X[:, 1].min() - 0.5, self.X[:, 1].max() + 0.5
        xx, yy = np.meshgrid(np.linspace(x_min, x_max, 300), np.linspace(y_min, y_max, 300))
        Z = self.model.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)

        return Z

    def get_model_accuracy_score(self, predictions):
        return accuracy_score(self.y, predictions)

    def get_model_precision_score(self, predictions):
        return precision_score(self.y, predictions, zero_division=0)

    def get_model_recall_score(self, predictions):
        return recall_score(self.y, predictions, zero_division=0)

    def get_model_f1_score(self, predictions):
        return f1_score(self.y, predictions, zero_division=0)
