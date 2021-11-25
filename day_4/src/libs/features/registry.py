
# src/libs/features/registry.py
from src.exception import FeatureNotFoundError


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
        yield feature_data
    
    def register(  # TODO 1. : define the method's signature):

        def do_register(  # TODO 2. : define the closure's signature):
        # TODO 3. : build a record to store in `self._registry`

        # A record is an instance of the FeatureRecord dataclass.
        #  - name: the name of the feature
        #  - func: the callable function
        #  - depends: the list of required dependencies
        #  - resources: the list of required external resources

        # TODO 4. : store the record in the instance state,
        # ie, in `self._registry` (a dict)
        # Records must be accessible by their names

        return  # TODO 5. : what should the `register` method return?