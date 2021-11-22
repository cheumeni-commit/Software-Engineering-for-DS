import logging

from src.config import config
from src.io import get_data_catalog
import pandas as pd

from src.constants import (
    DATE,
    PRODUCT_ID,
    GROSS_PRICE,
    NB_SOLD_PIECES,
	PERIOD_W,
	PRODUCT_NAME,
	COLOR,
	PERIOD_Y
)


logger = logging.getLogger(__name__)


def _get_daily_transactions(transactions):
	"Aggregate daily transactions"
	return (transactions.groupby([PRODUCT_ID, DATE])[NB_SOLD_PIECES].agg('sum').reset_index())


def _get_weekly_transactions(daily_transactions):
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

	catalog = get_data_catalog()
	# daily transaction
	daily_tx = _get_daily_transactions(catalog['transactions'])
	# weekly transaction
	weekly_tx = _get_weekly_transactions(daily_tx)
	# year transaction
	year_tx = _get_year_transactions(weekly_tx)
	# aggregation transactions
	agg_transaction = _get_transactions(year_tx)
	# merge aggregation transaction with product
	dataset_merge = _merge_transactions_with_products(agg_transaction, catalog['products'])
    # Update column DATE 
	dataset_merge[DATE] = pd.to_datetime(dataset_merge[PERIOD_W].astype(str)+
	                dataset_merge[PERIOD_Y].astype(str).add('-1'),format = "%W%Y-%w")
	# drop supplier
	dataset = dataset_merge.drop('supplier', axis=1)

	return dataset