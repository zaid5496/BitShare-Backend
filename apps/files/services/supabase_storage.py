from pathlib import Path

from django.conf import settings

from supabase import create_client

from .storage_backend import (
    StorageBackend,
)


class SupabaseStorage(
    StorageBackend
):

    def __init__(self):

        self.client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY,
        )

        self.bucket = (
            settings.SUPABASE_BUCKET
        )

    def upload_chunk(
        self,
        node,
        file_id,
        chunk_index,
        data,
    ):

        object_name = (
            f"{node.name}/"
            f"{file_id}_"
            f"{chunk_index}.chunk"
        )

        self.client.storage.from_(
            self.bucket
        ).upload(
            object_name,
            data,
            {
                "content-type":
                "application/octet-stream"
            },
        )

        return object_name

    def download_chunk(
        self,
        path,
    ):

        return (
            self.client.storage
            .from_(self.bucket)
            .download(path)
        )

    def delete_chunk(
        self,
        path,
    ):

        self.client.storage.from_(
            self.bucket
        ).remove(
            [path]
        )

    def chunk_exists(
        self,
        path,
    ):

        try:

            folder = str(
                Path(path).parent
            )

            filename = (
                Path(path).name
            )

            files = (
                self.client.storage
                .from_(self.bucket)
                .list(folder)
            )

            return any(
                f["name"]
                == filename
                for f in files
            )

        except Exception:

            return False