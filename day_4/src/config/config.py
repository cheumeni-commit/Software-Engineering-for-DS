# src/config.py
from dataclasses import dataclass
import logging
import yaml

from src.config.directories import directories as dirs
from src.utils.deepmerge import deepmerge
from src.context import context


_CONFIG_FILENAME_DEV = ['config/config.yml', 'config/dev.yml']
_CONFIG_FILENAME_PRO = ['config/config.yml', 'config/production.yml']
root_dir = "/home/ubuntu/software-engineering-for-ds/day_2"

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class Config:
    target: str
    date_col: str
    test_cutoff: str
    features: dict
    model: dict


def load_config_file(_CONFIG_FILENAME):

    read_data = []
    try:
        for path in _CONFIG_FILENAME:
            with open(root_dir + "/" + path, 'r') as fp:
                read_data.append(yaml.safe_load(fp))
    except:
            logger.info("yml file don't find inside directories")

    return read_data


def context_choice(ENV):

    if ENV == 'dev':
        read_data = load_config_file(_CONFIG_FILENAME_DEV)
    else:
        read_data = load_config_file(_CONFIG_FILENAME_PRO)
    return read_data


def get_config(env: str) -> Config:
    
    configs = context_choice(env)
    config = deepmerge(*configs)

    return Config(**config)
