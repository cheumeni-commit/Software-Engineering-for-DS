
import logging
from sklearn.ensemble import RandomForestRegressor

from src.config import config

_MODELS_REGISTRY_ = {'RandomForest': RandomForestRegressor}

logger = logging.getLogger(__name__)


def get_model(config):
    'Get model'

    try:
        Model = _MODELS_REGISTRY_[config.model['name']]
    except:
        logger.info("The model is not available ")

    return Model(**config.model['params'])
