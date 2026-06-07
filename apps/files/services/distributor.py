from apps.files.models import (
    FileChunk,
    ChunkReplica,
)

from .chunker import split_file
from .storage_factory import get_storage
from .node_selector import get_nodes_for_chunk

from apps.common.constants import (
    REPLICATION_FACTOR,
)
from apps.files.tasks import (
    remove_original_file
)


def distribute_file(file_obj):

    chunks = split_file(
        file_obj.file.path
    )
    storage = get_storage()
    for chunk in chunks:

        file_chunk = FileChunk.objects.create(
            file=file_obj,
            chunk_index=chunk["index"],
            checksum=chunk["checksum"],
            chunk_size=chunk["size"],
        )

        nodes = get_nodes_for_chunk(
            f"{file_obj.id}-{chunk['index']}"
        )

        for node in nodes:

            stored_path = (
                storage.upload_chunk(
                    node,
                    file_obj.id,
                    chunk["index"],
                    chunk["data"],
                )
            )

            ChunkReplica.objects.create(
                chunk=file_chunk,
                node=node,
                path=stored_path,
            )

    file_obj.is_distributed = True
    file_obj.save(update_fields=["is_distributed"])

    remove_original_file.delay(file_obj.id)