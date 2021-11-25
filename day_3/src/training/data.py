import logging

import pandas as pd

from src.config.config import get_config
from src.config.directories import directories
from src.io import get_data_catalog, save_dataset
from src.io import load_products, load_transactions
from src.libs.dag.graph import Graph


from src.constants import (
    DATE,
    PRODUCT_ID,
    GROSS_PRICE,
    NB_SOLD_PIECES,
	PERIOD_W,
	PRODUCT_NAME,
	COLOR,
	PERIOD_Y,
	DATASET
)


logger = logging.getLogger(__name__)


def _compute_daily_transactions(transactions):
	"Aggregate daily transactions"
	return (transactions.groupby([PRODUCT_ID, DATE])[NB_SOLD_PIECES].agg('sum').reset_index())


def _compute_weekly_transactions(daily_transactions):
	"Aggregate on weekly over daily transactions"
	daily_transactions[PERIOD_W] = pd.to_datetime(daily_transactions[DATE]).dt.week
	return daily_transactions

def _get_year_transactions(week_transactions):
	"Aggregate on weekly over year transactions"
	week_transactions[PERIOD_Y] = pd.to_datetime(week_transactions[DATE]).dt.year
	return week_transactions

def _get_transactions(year_transactions):
	"Aggregate on weekly over transactions"
	year_transactions=year_transactions.groupby(
    [PRODUCT_ID, PERIOD_W, PERIOD_Y])[NB_SOLD_PIECES].agg('sum').reset_index()
	return year_transactions

def _merge_transactions_with_products(agg_transactions, products):
	"Merge transaction with product on product_id"
	return agg_transactions.merge(products, on= PRODUCT_ID).drop([PRODUCT_NAME, COLOR], axis=1)
	

def build_dataset():

	"Build dataset with daily and weekly transactions"
	
	pipeline = Graph()

	pipeline.add_edge(_compute_daily_transactions, load_transactions)
	pipeline.add_edge(_compute_weekly_transactions, _compute_daily_transactions)

	pipeline.add_edge(_get_year_transactions, _compute_weekly_transactions)
	pipeline.add_edge(_get_transactions, _get_year_transactions)

	pipeline.add_edge(_merge_transactions_with_products, load_products)
	pipeline.add_edge(_merge_transactions_with_products, _get_transactions)
    
	pipeline.add_edge(_save_dataset, _merge_transactions_with_products)

	return pipeline 


def _save_dataset(dataset):
    path = directories.raw_data_dir/ DATASET
	# Add date column
    dataset[DATE] = pd.to_datetime(dataset[PERIOD_W].astype(str)+
	                dataset[PERIOD_Y].astype(str).add('-1'),format = "%W%Y-%w")
	# drop supplier
    dataset = dataset.drop('supplier', axis=1)

    return save_dataset(dataset, path=path)