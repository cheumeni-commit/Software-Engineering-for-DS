import logging

from src.io import get_data_catalog

logger = logging.getLogger(__name__)

class Executor:
    def __init__(self):
        self._states = {}
        
    def execute(self, graph):
        for node in graph.topo_sorted():

            dep = graph.get_node_dependencies(node)
            next_input = (self._states[d] for d in dep)
            self._states[node] = node(*next_input)
            
            last_node = node
        logger.info(f"Successfully executed {graph}.")
        return self._states[last_node]
            
