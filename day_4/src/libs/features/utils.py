# src/libs/features/utils.py
from types import GeneratorType


def chain_from_iterables(iterables, unpacked_types=()):
    """Like itertools.chain.from_iterable, but avoid unpacking np arrays."""
    for it in iterables:
        if isinstance(it, unpacked_types):
            yield from it
        else:
            yield it

            