from pathlib import Path

from .storage_backend import (
    StorageBackend,
)


class LocalDiskStorage(
    StorageBackend
):

    def upload_chunk(
        self,
        node,
        file_id,
        chunk_index,
        data,
    ):

        node_path = Path(
            node.base_path
        )

        node_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        chunk_name = (
            f"{file_id}_"
            f"{chunk_index}.chunk"
        )

        chunk_path = (
            node_path
            / chunk_name
        )

        with open(
            chunk_path,
            "wb",
        ) as f:

            f.write(data)

        return str(chunk_path)

    def download_chunk(
        self,
        path,
    ):

        with open(
            path,
            "rb",
        ) as f:

            return f.read()

    def delete_chunk(
        self,
        path,
    ):

        path = Path(path)

        if path.exists():

            path.unlink()