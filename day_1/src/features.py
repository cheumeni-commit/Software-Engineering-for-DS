# src/features.py
import numpy as np 
import pandas as pd

from src.constants import (
    DATE,
    PRODUCT_ID,
    GROSS_PRICE,
    NB_SOLD_PIECES,
    PERIOD_W,
    PERIOD_Y,
    PERIOD_Q,
    LAG,
    NB_WEEK

)

def build_feature_set(data):

    # create column of lag_target
    for lag in LAG:
        data = _lag_traget(data, lag)

    # create column of rolling column
    data = _rolling_mean_3W(data)
    data = _rolling_mean_4W(data)
    data = _rolling_mean_5W(data)
    
    # create column of feature sin 
    data = _sin_transformation(data)
 
    # create column of feature sin 
    data = _cos_transformation(data)
    
    return data

def _lag_traget(data, lag):

    data[f'lag_target_{lag}W'] = (data.groupby('product_id')['nb_sold_pieces'] \
            .transform(lambda x:x.shift(lag))).fillna(method='bfill')
    
    return data


def _rolling_mean_3W(data):
    data[f'rolling_mean_3W'] = np.mean(data[['lag_target_1W', 'lag_target_2W', 'lag_target_3W']], axis=1)
    return data


def _rolling_mean_4W(data):
    data[f'rolling_mean_4W'] = np.mean(data[['lag_target_1W', 'lag_target_2W', 'lag_target_3W', 
                                'lag_target_4W']], axis=1)
    return data


def _rolling_mean_5W(data):
    data[f'rolling_mean_5W'] = np.mean(data[['lag_target_1W', 'lag_target_2W', 'lag_target_3W',
                              'lag_target_4W', 'lag_target_5W']], axis=1)
    return data


def _sin_transformation(data):
    data['sin_week'] = np.sin((data[PERIOD_W]-1) * np.pi *2 / (52+71 / 400))
    return data


def _cos_transformation(data):
    data['cos_week'] = np.cos((data[PERIOD_W]-1) * 2*np.pi /(52+(71 / 400)))
    return data
