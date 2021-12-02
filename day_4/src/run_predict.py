# src/run_predict.py
"""
Prediction pipeline
"""
import time
import logging

from src.prediction.main import predict

logger = logging.getLogger(__name__)


def main():
    start = time.time()
    logger.info("Starting prediction job...")
    
    predictions = predict()
    # Maybe you don't have a 'save_predictions' function... That's OK.
    # You can implement it as a bonus :)
    save_predictions(predictions)

    run_duration = time.time() - start
    logger.info("Prediction job done.")
    logger.info(f"Prediction took {run_duration:.2f}s to execute")


if __name__ == '__main__':
    main()