# src/libs/dag/utils.py
import networkx as nx

from typing import Callable, Mapping, Dict, Iterable, Any


def map_adjacency(
    func: Callable, 
    adjacency: Mapping[Any, Iterable]) -> Dict[Any, Iterable]:
    """An improved version of the built-in map.

    Return a dictionary whose keys are `func(key)` and 
    values are `func` applied to every element of 
    the given mapping values.

    Args:
        func: a callable
        adjacency: a mapping that has exclusively iterable values.
    """
    return {
        func(key): [func(v) for v in values]
        for key, values in adjacency.items()
    }

def convert_to_networkx(graph):
    # need to reverse because of our implementation choices
    return nx.DiGraph(graph.edges).reverse()

    