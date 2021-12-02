# src/__main__.py
import logging
import argparse

import pandas as pd

from src.config import config
from src.io import get_data_catalog
from src.cli import main_cli

parser = argparse.ArgumentParser()
logger = logging.getLogger(__name__)

parser.add_argument('command', choices=['run_dataset', 'run_train'])
parser.add_argument('--show-time', action='store_true')

if __name__ == '__main__':

    args = parser.parse_args()
    main_cli(args)


    