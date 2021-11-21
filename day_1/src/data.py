import logging

from src.config import config
from src.io import get_data_catalog
import pandas as pd

from src.constants import (
    DATE,
    PRODUCT_ID,
    GROSS_PRICE,
    NB_SOLD_PIECES,
	PERIOD
)


logger = logging.getLogger(__name__)


def _get_daily_transactions(transactions):
	"Aggregate daily transactions"
	return (transactions.groupby([DATE, PRODUCT_ID])[NB_SOLD_PIECES].agg('sum').reset_index())


def _get_weekly_transactions(daily_transactions):
	"Aggregate on weekly over daily transactions"
	return (daily_transactions.set_index(DATE).to_period(freq='W').reset_index().rename(columns={DATE: PERIOD})).groupby([PRODUCT_ID, PERIOD], as_index=False)[config.target].agg('sum')


def _merge_transactions_with_products(weekly_transactions, products):
	"Merge transaction with product on product_id"
	return pd.merge(products, weekly_transactions, on='product_id')
	

def build_dataset():
	"Build dataset with daily and weekly transactions"

	catalog = get_data_catalog()
	
	daily_tx = _get_daily_transactions(catalog['transactions'])
	weekly_tx = _get_weekly_transactions(daily_tx)
	dataset = _merge_transactions_with_products(weekly_tx, catalog['products'])

	return dataset