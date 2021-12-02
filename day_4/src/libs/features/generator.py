# src/libs/features/generator.py
import logging
from types import GeneratorType

import pandas as pd

from src.libs.features.utils import chain_from_iterables

logger = logging.getLogger(__name__)

_TYPES_TO_UNPACK = (tuple, list, GeneratorType)


class FeaturesGenerator:

    def __init__(self, registry, features=None):
        self._registry = registry
        self.features = features or list(registry.registry.keys())
        self._state = {}

    def transform(self, data):
        for feature_name in self._registry:
            logger.debug(f"Generating feature '{feature_name}'...")

            record = self._registry.get(feature_name)

            deps = self._registry.get_feature_dependencies(record.name)

            upstream_data = self._chain_from_iterables(
                self._state[d] for d in deps if d
            )
            output = record.func(*self._chain_from_iterables(
                (data, upstream_data))
            )
            self._state[record.name] = output

        return pd.DataFrame({
            feature_name: self._state[feature_name]
            for feature_name in self.features
        })

    @staticmethod
    def _chain_from_iterables(iterables):
        return chain_from_iterables(iterables, _TYPES_TO_UNPACK)