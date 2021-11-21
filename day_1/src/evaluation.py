import numpy as np
from sklearn.metrics import r2_score


def r2(actual, predicted):
    return r2_score(actual, predicted)


def WAPE(actual, predicted):
    return np.sum(np.abs(actual - predicted)) / np.sum(actual)


_METRICS = {
    'r2': r2,
    'WAPE': WAPE
}


def train_test_split(dataset, *, date_col, cutoff):
    train, test = (
        dataset.loc[dataset[date_col] < cutoff],
        dataset.loc[dataset[date_col] >= cutoff]
    )
    return train, test


def evaluate_model(fitted_model, *, X, y):
    y_hat = fitted_model.predict(X)
    metrics = {name: func(y, y_hat) for name, func in _METRICS.items()}
    return metrics