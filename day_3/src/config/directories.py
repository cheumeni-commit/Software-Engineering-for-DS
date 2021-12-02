# src/directories.py
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class _Directories:

    def __init__(self):

        self.root_dir = Path(__file__).parents[1].resolve()
        self.package_dir = self.root_dir 
        self.data_dir = self.package_dir / 'data'
        self.raw_data_dir = self.data_dir / 'raw'
        self.raw_store_dir = self.data_dir / 'artefacts'

        for dir_path in vars(self).values():
            try:
                dir_path.mkdir(exist_ok=True, parents=True)
            except:
                logger.info("Error when we are build a {} directory".format(dir_path))


directories = _Directories()