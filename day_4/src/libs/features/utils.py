# src/libs/features/utils.py
from types import GeneratorType

TYPES_TO_UNPACK = (tuple, list, GeneratorType)

def chain_from_iterables(iterables):
    """Like itertools.chain.from_iterable, but avoid unpacking np arrays."""
    for it in iterables:
        if isinstance(it, TYPES_TO_UNPACK):
            yield from it
        else:
            yield it

            