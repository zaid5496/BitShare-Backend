import hashlib

from apps.files.models import StorageNode


class ConsistentHashRing:

    def __init__(self):

        self.ring = {}

        self.sorted_keys = []

        self._build_ring()

    def _hash(self, key):

        return int(
            hashlib.md5(
                str(key).encode()
            ).hexdigest(),
            16,
        )

    def _build_ring(self):

        nodes = (
            StorageNode.objects
            .filter(is_active=True)
        )

        for node in nodes:

            key = self._hash(
                node.name
            )

            self.ring[key] = node

            self.sorted_keys.append(
                key
            )

        self.sorted_keys.sort()

    def get_node(self, chunk_key):

        if not self.sorted_keys:
            raise Exception(
                "No storage nodes available."
            )

        hash_key = self._hash(
            chunk_key
        )

        for node_key in self.sorted_keys:

            if hash_key <= node_key:

                return self.ring[
                    node_key
                ]

        return self.ring[
            self.sorted_keys[0]
        ]
    

    def get_nodes(
        self,
        chunk_key,
        replication_factor=2,
    ):

        if not self.sorted_keys:
            raise Exception(
                "No nodes available."
            )

        hash_key = self._hash(
            chunk_key
        )

        start_idx = 0

        for i, node_key in enumerate(
            self.sorted_keys
        ):
            if hash_key <= node_key:
                start_idx = i
                break

        selected = []

        for i in range(
            replication_factor
        ):

            node_key = self.sorted_keys[
                (
                    start_idx + i
                )
                % len(self.sorted_keys)
            ]

            selected.append(
                self.ring[node_key]
            )

        return selected