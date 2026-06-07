from pathlib import Path

from apps.files.models import (
    FileChunk,
    ChunkReplica,
)

from .node_selector import (
    get_nodes_for_chunk,
)

from .storage_factory import (
    get_storage,
)


def rebalance_chunk(chunk):

    storage = get_storage()

    desired_nodes = {
        node.id
        for node in get_nodes_for_chunk(
            f"{chunk.file_id}-{chunk.chunk_index}"
        )
    }

    current_replicas = (
        chunk.replicas.select_related(
            "node"
        )
    )

    current_nodes = {
        replica.node_id
        for replica in current_replicas
    }

    if desired_nodes == current_nodes:
        return

    source_replica = None

    for replica in current_replicas:

        if storage.chunk_exists(replica.path):
            source_replica = replica
            break

    if not source_replica:
        return

    chunk_data = storage.download_chunk(
        source_replica.path
    )

    # Remove replicas that shouldn't exist
    for replica in current_replicas:

        if (
            replica.node_id
            not in desired_nodes
        ):

            storage.delete_chunk(
                replica.path
            )

            replica.delete()

    existing_nodes = {
        replica.node_id
        for replica in chunk.replicas.all()
    }

    desired_node_objects = (
        get_nodes_for_chunk(
            f"{chunk.file_id}-{chunk.chunk_index}"
        )
    )

    # Create missing replicas
    for node in desired_node_objects:

        if node.id in existing_nodes:
            continue

        stored_path = (
            storage.upload_chunk(
                node,
                chunk.file_id,
                chunk.chunk_index,
                chunk_data,
            )
        )

        ChunkReplica.objects.get_or_create(
            chunk=chunk,
            node=node,
            defaults={
                "path": stored_path,
            },
        )


def rebalance_cluster():

    for chunk in (
        FileChunk.objects.all()
    ):
        rebalance_chunk(chunk)