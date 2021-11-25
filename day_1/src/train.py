import logging

import pandas as pd

logger = logging.getLogger(__name__)

from src.config import config
from src.features import build_feature_set
from src.evaluation import evaluate_model
from sklearn.model_selection import train_test_split
from src.constants import (SIZE, NB_SOLD_PIECES, PERIOD,
                            DATE)


def train(model, dataset):

    # Add more feature for training
    dataset_with_feature = build_feature_set(dataset)
    # Split the data set
    X_train, y_train, X_test, y_test = _split_target(dataset_with_feature)

    logger.info(f"Train's shape: {X_train.shape}")
    logger.info(f"Test's shape: {X_test.shape}")

    logger.info(f"Training model...")
    fitted_model = _train_model(model, X=X_train, y=y_train)
    logger.info("Model trained.")

    train_metrics, test_metrics = (
        evaluate_model(fitted_model, X=X_train, y=y_train)
        for features in ((X_train, y_train), (X_test, y_test))
    )

    metrics_msg = "=" * 20 + " Metrics " + "=" * 20
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


def _split_target(features_set):
    
    features_set.sort_values(by=DATE)
    
    df_train, df_preds = _split_train_test(features_set)

    y_train = df_train.pop(NB_SOLD_PIECES)
    X_train = df_train[[c for c in df_train.columns if c != PERIOD]].drop(DATE,axis=True, inplace=False)

    y_test = df_preds.pop(NB_SOLD_PIECES)
    X_test = df_preds[[c for c in df_train.columns if c != PERIOD]].drop([DATE], axis=True)

    return X_train, y_train, X_test, y_test


def _split_train_test(features_set):

    df_train, df_test = train_test_split(features_set, test_size = SIZE)

    return df_train, df_test


def _train_model(model, X, y):
    model.fit(X, y)
    return model