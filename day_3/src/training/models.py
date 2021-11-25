
import logging
from sklearn.ensemble import RandomForestRegressor

from src.config.config import get_config

_MODELS_REGISTRY_ = {'RandomForest': RandomForestRegressor}

logger = logging.getLogger(__name__)


def get_model(directories, env):
    
    """ Load Model """

    try:
        Model = _MODELS_REGISTRY_[get_config(env).model['name']]
    except:
        logger.info("The model is not available ")

    return Model(** get_config(env).model['params'])
