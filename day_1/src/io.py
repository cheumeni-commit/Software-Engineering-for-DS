# src/io.py
import logging

import pandas as pd

from src.config import config
from src.constants import (
    PRODUCTS,
    TRANSACTIONS,
    DATE
)

logger = logging.getLogger(__name__)


def get_data_catalog():
    """ Return a dictionnary whose values are raw data as dataframes """

    logger.info("Loading data catalog...")

    products = pd.read_csv(config.raw_data_dir / PRODUCTS)
    transactions = pd.read_csv(
        config.raw_data_dir / TRANSACTIONS,
        parse_dates=[DATE]
    )

    logger.info("Data catalog loaded. ✅")

    return {
        'products': products,
        'transactions': transactions
    }


def save_dataset(dataset, *, path):
    dataset.to_csv(path, index=False)
    logger.info(f"Dataset saved at {path.relative_to(config.root_dir)}")

