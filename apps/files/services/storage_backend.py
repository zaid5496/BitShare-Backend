from abc import ABC
from abc import abstractmethod


class StorageBackend(ABC):

    @abstractmethod
    def upload_chunk(
        self,
        node,
        file_id,
        chunk_index,
        data,
    ):
        pass

    @abstractmethod
    def download_chunk(
        self,
        path,
    ):
        pass

    @abstractmethod
    def delete_chunk(
        self,
        path,
    ):
        pass