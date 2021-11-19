# src/run_dataset.py
from src.io import save_dataset
from src.config import config
from src.data import build_dataset

def main():
    "Generate dataset and store it on disk as a csv file"
    logger.info("Building dataset...")
    dataset = build_dataset()
    print("url dataset", config.raw_data_dir)
    save_dataset(dataset, config.raw_data_dir)

if __name__ == '__main__':
    main()