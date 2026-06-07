from django.db import models
from django.conf import settings
from django.utils import timezone

class File(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="files", null=True, blank=True)
    file = models.FileField(upload_to="uploads/")
    original_name = models.CharField(max_length=255)
    file_size = models.BigIntegerField()
    is_temporary = models.BooleanField(default=False)
    delete_after = models.DateTimeField(null=True, blank=True)
    is_distributed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.original_name
    
    class Meta:
        ordering = ["-created_at"]


class FileChunk(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name="chunks")
    chunk_index = models.PositiveIntegerField()
    checksum = models.CharField(max_length=64)
    chunk_size = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["chunk_index"]

    def __str__(self):
        return (
            f"{self.file_id}"
            f"-chunk-{self.chunk_index}")

    @property
    def replica_count(self):

        return self.replicas.count()


class StorageNode(models.Model):
    name = models.CharField(max_length=100)
    base_path = models.CharField(max_length=500)
    is_active = models.BooleanField(default=True)
    total_space = models.BigIntegerField(default=0)
    used_space = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    last_heartbeat = models.DateTimeField(null=True, blank=True,)
    
    def heartbeat(self):
        self.last_heartbeat = (timezone.now())
        self.save(update_fields=["last_heartbeat"])


class ChunkReplica(models.Model):
    chunk = models.ForeignKey(FileChunk, on_delete=models.CASCADE, related_name="replicas")
    node = models.ForeignKey(StorageNode, on_delete=models.CASCADE)
    path = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.chunk_id}"
            f" -> "
            f"{self.node.name}"
        )
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "chunk",
                    "node",
                ],
                name=(
                    "unique_chunk_node"
                ),
            ),
        ]