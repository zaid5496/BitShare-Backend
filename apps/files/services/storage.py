from pathlib import Path


def store_chunk(
    node_path,
    file_id,
    chunk_index,
    data,
):

    node_path = Path(node_path)

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
        "wb"
    ) as f:
        f.write(data)

    return str(chunk_path)