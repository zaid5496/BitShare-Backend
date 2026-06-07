from apps.common.constants import (
    REPLICATION_FACTOR,
)

from .hash_ring import (
    ConsistentHashRing,
)


def get_nodes_for_chunk(
    chunk_key,
):

    ring = ConsistentHashRing()

    return ring.get_nodes(
        chunk_key,
        REPLICATION_FACTOR,
    )