# src/config.py
from pathlib import Path
from src.constants import NB_SOLD_PIECES, PERIOD

class _Config:

    def __init__(self):
        self.root_dir = Path(__file__).parents[1].resolve()
        self.package_dir = self.root_dir / 'src'
        self.data_dir = self.package_dir / 'data'
        self.raw_data_dir = self.data_dir / 'raw'
        self.target = NB_SOLD_PIECES

        self.date_col = PERIOD
        self.test_cutoff = '06-02-2018'

        self.model = {
            'name': 'RandomForest',
            'params': {
                'n_estimators': 100,
            }
        }

config = _Config()