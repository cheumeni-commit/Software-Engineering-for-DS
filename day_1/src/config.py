# src/config.py
from pathlib import Path
from src.constants import NB_SOLD_PIECES

class _Config:

    def __init__(self):
        self.root_dir = Path(__file__).parents[1].resolve()
        self.package_dir = self.root_dir / 'src'
        self.data_dir = self.root_dir / 'data'
        self.raw_data_dir = self.data_dir / 'raw'
        self.target = NB_SOLD_PIECES

config = _Config()