# src/libs/features/generator.py
import pandas as pd

from src.libs.features.utils import chain_from_iterables


class FeaturesGenerator:

    def __init__(self, registry, features=None, resources=None):
        self.registry = registry
        # Note: our naming is a bit confusing... There is room
        # for improvements... but later.

        self.features = features or list(registry.registry.keys())
        self.resources = resources or []
        self._state = {}
        # TODO 0. we miss something to keep track of the execution...
        #         Add it!

    def transform(self, data):

        for feature_name in self.registry:

            logger.debug(f"Generating feature '{feature_name}'...")

            record = self.registry.get(feature_name)

            deps = self.registry.get_feature_dependencies(record.name)

            # unpack data from deps output. You're welcome!
            upstream_data = chain_from_iterables(
                self._state[d] for d in deps if d
            )

            # TODO 2. run the transform process
            # on the feature, and fetch its output.
            output =  record.func(chain_from_iterables(
                (data, upstream_data))
            )
           
            # TODO 3. store the output in instance's state
            # It must be accessible by feature name.
            self._state[record.name] = output

        logger.debug("Feature generation done!")
        # TODO 4. return a pandas DataFrame whose columns are
        # the feature names, and values are the output of the
        # `transform` processing.

        return pd.DataFrame({feature_name: self._state[feature_name]
                            for feature_name in self.features})