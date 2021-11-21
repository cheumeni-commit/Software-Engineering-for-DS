import logging

import pandas as pd

logger = logging.getLogger(__name__)

from src.config import config
from src.features import build_feature_set
from src.evaluation import train_test_split, evaluate_model


def train(model, dataset):
    train_data, test_data = train_test_split(
        dataset,
        date_col=config.date_col,
        cutoff=config.test_cutoff
    )
    logger.info(f"Train's shape: {train_data.shape}")
    logger.info(f"Test's shape: {test_data.shape}")

    # NOTE: This unpacking is not the most elegant.
    #       We'll explore ways to handle those things later in the training
    #
    #       An alternative would be to not use comprehension and
    #       simply call each function twice.
    #       Although it might make the code harder to read,
    #       I favored the shorter version because the function is already
    #       quite long.
    ((X_train, y_train), (X_test, y_test)) = (
        _split_target(build_feature_set(data), target=config.target)
        for data in (train_data, test_data)
    )

    logger.info(f"Training model...")
    fitted_model = _train_model(model, X=X_train, y=y_train)
    logger.info("Model trained.")

    train_metrics, test_metrics = (
        evaluate_model(fitted_model, X=X_train, y=y_train)
        for features in ((X_train, y_train), (X_test, y_test))
    )

    metrics_msg = "=" * 10 + " Metrics " + "=" * 10
    logger.info(metrics_msg)
    logger.info(f"Train: {train_metrics}")
    logger.info(f"Test: {test_metrics}")
    logger.info("=" * len(metrics_msg))
    
    return {
        'model': fitted_model,
        'metrics': {
            'train': train_metrics,
            'test': test_metrics
        }
    }


def _split_target(features_set, *, target):
    X = features_set.copy()
    # NOTE: pop mutates X
    y = X.pop(target)
    return X, y


def _train_model(model, *, X, y):
    model.fit(X, y)
    return model