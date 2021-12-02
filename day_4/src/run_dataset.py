# src/run_dataset.py
import logging

from src.libs.dag.executor import Executor
from src.io import save_dataset
from src.training.data import build_datasets


logger = logging.getLogger(__name__)

def main_dataset():
    "Generate dataset and store it on disk as a csv file"
    logger.info("Building dataset...")
    pipeline = build_datasets()
    executor = Executor()
    dataset = executor.execute(pipeline)

    #print("url dataset", directories.raw_data_dir)
    #save_dataset(dataset, path=directories.raw_data_dir/ DATASET)

if __name__ == '__main__':
    main_dataset()