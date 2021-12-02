import matplotlib.pyplot as plt
import networkx as nx   # install it if missing: !pip install networkx

###################################################################
# Our pipelines need an up-to-date context to work.
from src.config.config import get_config
from src.context import context


context.environment = 'development'  # or 'dev', depends on your config files
context.config = get_config(context)
###################################################################

def draw_graph(graph, *, ax=None, save_path=None):
    if ax is None:
        ax = plt.axes()
    # NOTE: 
    # We need `.reverse` here because we have reversed
    # our adjacency list for convenience. You shouldn't
    # care about that detail.
    nx_graph = nx.DiGraph(graph.edges).reverse()
    nx.draw_networkx(nx_graph, ax=ax)
    if save_path is not None:
        ax.figure.savefig(save_path)

    return ax

###################################################################

from src.training.data import build_dataset  # the graph used for testing
graph = build_dataset()

###################################################################
draw_graph(graph);  # use the ';' for nicer display