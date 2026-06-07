import uuid
from apps.files.models import File
from django.db import models


class ShareLink(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name="share_links")
    password_hash = models.CharField(max_length=255, blank=True, null=True)
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    expires_at = models.DateTimeField()
    max_downloads = models.PositiveIntegerField(default=1)
    current_downloads = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.token)