# src/io.py
import logging
import joblib  # or pickle.
import json

import pandas as pd

from src.config.directories import directories
from src.constants import (
    PRODUCTS,
    TRANSACTIONS,
    SAVE_MODEL,
    SAVE_METRICS,
    DATE
)


logger = logging.getLogger(__name__)


def get_data_catalog():
    """ Return a dictionnary whose values are raw data as dataframes """

    logger.info("Loading data catalog...")
    var = None

    if directories.raw_data_dir.is_dir:
        products = load_products()
        transactions = load_transactions()
        
        logger.info("Data catalog loaded. ✅")
        return {
            'products': products,
            'transactions': transactions
            }   
    else:
 	    logger.warning("Data file are not unload, please check")


   
def load_products():
    return pd.read_csv(directories.raw_data_dir / PRODUCTS)
    

def load_transactions():
    return pd.read_csv(
        	directories.raw_data_dir / TRANSACTIONS,
        	parse_dates=[DATE]
    	)


def save_dataset(dataset, *, path):

    dataset.to_csv(path, index=False)
    logger.info(f"Dataset saved at {path.relative_to(directories.root_dir)}")


def load_dataset(path):
    return pd.read_csv(path, parse_dates=True)


def save_model(model, *, path):
    logger.info("Model are saved")
    return joblib.dump(model, path)


def save_metrics(metrics, *, path):
    with open(path, 'w') as f:
        json.dump(metrics, f, indent=2)


def save_training_output(output, *, directory):

    store_model = save_model(output['model'], path = str(directory) + '/' + SAVE_MODEL)
    store_metrics = save_metrics(output['metrics'], path = str(directory) + '/' + SAVE_METRICS)


def load_model(path):
    return joblib.load(path)
    

def load_predictions_data(path):
    with open(path) as fp:
        return json.load(fp)




