from django.contrib import admin

from .models import (
    File,
    StorageNode,
    FileChunk,
    ChunkReplica,
)

admin.site.register(File)
admin.site.register(StorageNode)
admin.site.register(FileChunk)
admin.site.register(ChunkReplica)