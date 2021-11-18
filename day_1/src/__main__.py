# src/__main__.py
import logging

from src.config import config
from src.io import get_data_catalog
import pandas as pd


logger = logging.getLogger(__name__)

if __name__ == '__main__':

	#logger.debug("I'm testing the logging configuration.")
    #print(config.root_dir)  # just a sanity check 
    data = get_data_catalog()
    data = pd.DataFrame(data['transactions'])
    