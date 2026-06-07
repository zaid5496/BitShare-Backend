from rest_framework import serializers
from .models import File


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File

        fields = [
            "id",
            "original_name",
            "file_size",
            "file",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "original_name",
            "file_size",
            "created_at",
        ]