#!/usr/bin/env python3
"""
Model training script.
"""
import time
import logging

from src.config import config
from src.constants import DATASET
from src.io import load_dataset
from src.models import get_model
from src.train import train

logger = logging.getLogger(__name__)


def main_train():
    start = time.time()
    logger.info("Starting training job...")
    model = get_model(config)
    dataset_path = config.raw_data_dir / DATASET
    dataset = load_dataset(dataset_path)
    train(model, dataset)
    run_duration = time.time() - start
    logger.info("Training job done...")
    logger.info(f"Took {run_duration} seconds to execute")


if __name__ == '__main__':
    main_train()