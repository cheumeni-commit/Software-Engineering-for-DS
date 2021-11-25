#!/usr/bin/env python3
"""
Model training script.
"""
import time
import logging

from src.config.directories import directories
from src.constants import DATASET
from src.io import load_dataset, save_training_output
from src.training.models import get_model
from src.train import train


logger = logging.getLogger(__name__)


def main_train(env):
    start = time.time()
    logger.info("Starting training job...")
    model = get_model(directories, env)
   
    dataset_path = directories.raw_data_dir / DATASET
    dataset = load_dataset(dataset_path)
    model_metrics = train(model, dataset)
    save_training_output(model_metrics, directory=directories.raw_store_dir)
    run_duration = time.time() - start
    logger.info("Training job done...")
    logger.info(f"Took {run_duration} seconds to execute")


if __name__ == '__main__':
    main_train()