from pathlib import Path

from .storage_factory import (
    get_storage,
)


def reconstruct_file(
    file_obj,
    output_path,
):

    storage = get_storage()

    chunks = (
        file_obj.chunks
        .prefetch_related("replicas")
        .order_by("chunk_index")
    )

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        output_path,
        "wb",
    ) as output:

        for chunk in chunks:

            replica = None

            for candidate in (
                chunk.replicas.all()
            ):

                if storage.chunk_exists(
                    candidate.path
                ):

                    replica = candidate
                    break

            if not replica:

                raise Exception(
                    f"No valid replica found "
                    f"for chunk {chunk.id}"
                )

            output.write(
                storage.download_chunk(
                    replica.path
                )
            )

    return str(output_path)