import numpy as np
from sklearn.metrics import r2_score


def R2(actual, predicted):
    return r2_score(actual, predicted)


def WAPE(actual, predicted):
    return np.sum(np.abs(actual - predicted)) / np.sum(actual)


_METRICS = {
    'r2': R2,
    'WAPE': WAPE
}

def evaluate_model(fitted_model, *, X, y):

    y_pred = fitted_model.predict(X)
    metrics = {name: func(y, y_pred) for name, func in _METRICS.items()}
    return metrics