# src/run_dataset.py
import logging

from src.config import config
from src.data import build_dataset
from src.io import save_dataset
from src.constants import DATASET

logger = logging.getLogger(__name__)

def main_dataset():
    "Generate dataset and store it on disk as a csv file"
    logger.info("Building dataset...")
    dataset = build_dataset()
    print("url dataset", config.raw_data_dir)
    save_dataset(dataset, path=config.raw_data_dir/ DATASET)

if __name__ == '__main__':
    main_dataset()