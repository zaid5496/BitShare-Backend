from pathlib import Path

from .reassembler import reconstruct_file


DOWNLOAD_DIR = Path("/tmp/bitshare_downloads")


def build_download_file(file_obj):

    DOWNLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        DOWNLOAD_DIR
        / f"{file_obj.id}_{file_obj.original_name}"
    )

    reconstruct_file(
        file_obj,
        output_path,
    )

    return str(output_path)