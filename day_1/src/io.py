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

    if config.raw_data_dir.is_dir:

        products = pd.read_csv(config.raw_data_dir / PRODUCTS)

        transactions = pd.read_csv(
        	config.raw_data_dir / TRANSACTIONS,
        	parse_dates=[DATE]
    	)

        logger.info("Data catalog loaded. ✅")

    else:
 	    logger.warning("Data file are unload, please check")

    return {
        'products': products,
        'transactions': transactions
    }


def save_dataset(dataset, *, path):

    dataset.to_csv(path, index=False)
    logger.info(f"Dataset saved at {path.relative_to(config.root_dir)}")

def load_dataset(path):
    return pd.read_csv(path, parse_dates=True)