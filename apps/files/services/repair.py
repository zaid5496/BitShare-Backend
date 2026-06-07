from pathlib import Path

from apps.files.models import (
    FileChunk,
    ChunkReplica,
)

from apps.common.constants import REPLICATION_FACTOR
from apps.files.models import StorageNode
from .storage import store_chunk
from .storage_factory import get_storage

def repair_chunk(chunk):
    storage = get_storage()
    valid_replicas = []
    for replica in chunk.replicas.all():

        if storage.chunk_exists(replica.path):
            valid_replicas.append(replica)

    if len(valid_replicas) >= REPLICATION_FACTOR:
        return

    if not valid_replicas:
        print(f"Chunk {chunk.id} has no "f"valid replicas.")
        return

    source_replica = valid_replicas[0]

    chunk_data = (
        storage.download_chunk(
            source_replica.path
        )
    )

    used_node_ids = {
        replica.node_id
        for replica in valid_replicas
    }

    candidate_nodes = list(
        StorageNode.objects.filter(
            is_active=True
        ).exclude(
            id__in=used_node_ids
        )
    )

    needed = (
        REPLICATION_FACTOR
        - len(valid_replicas)
    )

    for node in candidate_nodes[:needed]:

        stored_path = (
            storage.upload_chunk(
                node,
                chunk.file_id,
                chunk.chunk_index,
                chunk_data,
            )
        )

        ChunkReplica.objects.create(
            chunk=chunk,
            node=node,
            path=stored_path,
        )


def repair_all_chunks():

    for chunk in FileChunk.objects.all():
        repair_chunk(chunk)