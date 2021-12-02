# src/libs/dag/graph.py
# https://docs.python.org/3/library/collections.html#collections.defaultdict
import networkx as nx
from collections import defaultdict

from src.libs.dag.utils import convert_to_networkx


class Graph:

    def __init__(self):

        self.edges = defaultdict(list)

    def add_edge(self, source, target):
        self.edges[target].append(source)

    def get_node_dependencies(self, node):
        return self.edges.get(node, [])

    def topo_sorted(self):
        nx_graph = convert_to_networkx(self)
        return nx.algorithms.dag.topological_sort(nx_graph)



    