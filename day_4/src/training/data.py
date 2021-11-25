import logging

import pandas as pd
import numpy as np

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
	LAG,
	HISTORICAL,
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

def _add_date_and_delete_supplier(dataset):
	# Add date column
    dataset[DATE] = pd.to_datetime(dataset[PERIOD_W].astype(str)+
	                dataset[PERIOD_Y].astype(str).add('-1'),format = "%W%Y-%w")
	# drop supplier
    dataset = dataset.drop('supplier', axis=1)
    return dataset


def _lagged(data, *, lag):

	data[f'lag_target_{lag}W'] = (data.groupby('product_id')['nb_sold_pieces'] \
			.transform(lambda x:x.shift(lag))).fillna(method='bfill')
	return data


def _moving_average(data, *, window):

	if window == 3:
		data[f'rolling_mean_3W'] = np.mean(data[['lag_target_1W', 'lag_target_2W',
		    'lag_target_3W']], axis=1)
		return data
	elif window == 4:
		data[f'rolling_mean_4W'] = np.mean(data[['lag_target_1W', 'lag_target_2W',
				'lag_target_3W', 'lag_target_4W']], axis=1)
		return data
	elif window == 5:
		data[f'rolling_mean_5W'] = np.mean(data[['lag_target_1W', 'lag_target_2W', 
			'lag_target_3W', 'lag_target_4W', 'lag_target_5W']], axis=1)
		return data
	else:
		logger.info("window is not correct, please check it")

def _compute_historical(transactions):

	# create column of lag_target
	for lag in LAG:
		transactions = _lagged(transactions, lag=lag)
	for window in [3, 4, 5]:
		transactions = _moving_average(transactions, window=window)

	return transactions


def _save_dataset(dataset):
    path = directories.raw_data_dir/ DATASET
    return save_dataset(dataset, path=path)


def _save_historical(historical):
    path = directories.raw_data_dir/ HISTORICAL
    return save_dataset(pd.DataFrame(historical), path=path)
	

def build_datasets():

	"Build dataset with daily and weekly transactions"
	
	pipeline = Graph()

	pipeline.add_edge(_compute_daily_transactions, load_transactions)

	pipeline.add_edge(_compute_weekly_transactions, _compute_daily_transactions)

	pipeline.add_edge(_get_year_transactions, _compute_weekly_transactions)
	pipeline.add_edge(_get_transactions, _get_year_transactions)

	pipeline.add_edge(_merge_transactions_with_products, load_products)
	pipeline.add_edge(_merge_transactions_with_products, _get_transactions)

	pipeline.add_edge(_add_date_and_delete_supplier, _merge_transactions_with_products)
    
	pipeline.add_edge(_save_dataset, _add_date_and_delete_supplier)

	pipeline.add_edge(_compute_historical, load_transactions)

	pipeline.add_edge(_save_historical, _compute_historical)

	return pipeline 
