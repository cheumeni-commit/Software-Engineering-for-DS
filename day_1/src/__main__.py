# src/__main__.py
import logging

import pandas as pd

from src.config import config
from src.io import get_data_catalog
from src.run_train import main
#from src.run_dataset import main


logger = logging.getLogger(__name__)

if __name__ == '__main__':

    logger.debug("I'm testing the logging configuration.")
    main()


    