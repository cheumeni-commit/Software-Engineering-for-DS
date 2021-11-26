
# src/libs/features/registry.py
import networkx as nx

from dataclasses import dataclass
from typing import Callable, List

from src.exceptions import FeatureNotFoundError


@dataclass
class FeatureRecord:
    name: str
    func: Callable
    depends: List[str]  # list of required dependency names
    resources: List[str]  # same with resources


class FeatureRegistry:  # or FeatureStore... as you prefer!

    def __init__(self):
        self._registry = {}

    @property
    def registry(self):  # avoid state mutation from outside
        return self._registry

    @property
    def adjacency(self):
        return {k: v.depends for k, v in self._registry.items()}

    def get_feature_dependencies(self, name):
        deps = self.adjacency.get(name)
        if deps is None:
            raise FeatureNotFoundError  # your custom error
        return deps

    def topo_sorted(self):
        nx_graph = nx.DiGraph(adjacency).reverse()
        return nx.algorithms.dag.topological_sort(nx_graph)

    def get(self, name):
        feature_data = self.registry[name]
        if feature_data is None:
            raise FeatureNotFoundError 
        return feature_data
    
    def register(self, name, *, depends=None, resources=None):

        depends = depends or []
        resources = resources or []

        def do_register(func):
            nonlocal name
            if name is None:
                name = func.__name__
            record = FeatureRecord(
                name=name,
                func=func,
                depends=list(depends),
                resources=list(resources)
            )
            self._registry[name] = record

        return do_register