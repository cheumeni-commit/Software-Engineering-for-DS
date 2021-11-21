# src/features.py
import numpy as np 
import pandas as pd

from src.contants import (
    DATE,
    PRODUCT_ID,
    GROSS_PRICE,
    NB_SOLD_PIECES,
    PERIOD_W,
    PERIOD_Y,
    PERIOD_Q,
    NB_WEEK

)

def build_feature_set(data):
    'Build feature engineering'

    data[DATE] = pd.to_datetime(data[PERIOD_W].astype(str) + data[PERIOD_Y].astype(str).add('-1'),format = "%W%Y-%w")
    data[PERIOD_Q] = data[DATE].dt.quarter
    # create column of lag_target
    data_with_lag_column = _lag_traget(data)

    # create column of rolling mean
    data_with_rollingmean_column = _rolling_mean(data_with_lag_column)

    # create column of feature sin, cos and supplier
    data_with_sincos_transformation = _another_transformation(data_with_rollingmean_column)

    return data_with_sincos_transformation

def _lag_traget(data):
    'lag target'

    for lag in range(1, NB_WEEK):
        data[f'lag_target_{lag}W'] = data.groupby(PRODUCT_ID)[NB_SOLD_PIECES].shift(lag)
        data[f'lag_target_{lag}W'] = data[f'lag_target_{lag}W'].fillna(method='bfill')
    
    return data

def _rolling_mean(data):
    'Build a rolling mean'

    data[f'rolling_mean_3W'] = np.mean(data[['lag_target_1W', 'lag_target_2W', 'lag_target_3W']], axis=1)
    data[f'rolling_mean_4W'] = np.mean(data[['lag_target_1W', 'lag_target_2W', 'lag_target_3W', 'lag_target_4W']],
                              axis=1)
    data[f'rolling_mean_5W'] = np.mean(data[['lag_target_1W', 'lag_target_2W', 'lag_target_3W', 'lag_target_4W', 'lag_target_5W']], axis=1)

    return data

def _another_transformation(data):
    'add many transformation'

    data['sin_week'] = np.sin((data[PERIOD_W]-1) * np.pi *2 / (52+71 / 400))
    data['cos_week'] = np.cos((data[PERIOD_W]-1) * 2*np.pi /(52+(71 / 400)))
    data['supplier'] = data['supplier'].fillna('UNKNOWN')
    data['supplier'] = data['supplier'].astype('category').cat.codes

    return data