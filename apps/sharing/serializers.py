from rest_framework import serializers

from .models import ShareLink


class ShareLinkSerializer(serializers.ModelSerializer):
    file_name = serializers.CharField(
        source="file.original_name",
        read_only=True
    )

    class Meta:
        model = ShareLink

        fields = [
            "id",
            "file_name",
            "token",
            "expires_at",
            "max_downloads",
            "current_downloads",
            "is_active",
            "created_at",
        ]