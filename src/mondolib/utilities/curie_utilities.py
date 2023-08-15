"""mondolib CURIE utilities."""
from oaklib.types import CURIE


def get_curie_prefix(curie: CURIE) -> str:
    """
    Get the prefix part of a CURIE, e.g. OMIM for OMIM:100000.

    :param curie:
    :return:
    """
    prefix, _ = curie.split(":")
    return prefix
