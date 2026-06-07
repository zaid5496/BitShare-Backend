import hashlib
from pathlib import Path


CHUNK_SIZE = 1024 * 1024  # 1 MB


def calculate_checksum(data):

    return hashlib.sha256(
        data
    ).hexdigest()


def split_file(file_path):

    file_path = Path(file_path)

    chunks = []

    with open(file_path, "rb") as f:

        chunk_index = 0

        while True:

            data = f.read(CHUNK_SIZE)

            if not data:
                break

            chunks.append(
                {
                    "index": chunk_index,
                    "data": data,
                    "size": len(data),
                    "checksum": calculate_checksum(data),
                }
            )

            chunk_index += 1

    return chunks