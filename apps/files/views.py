from django.http import FileResponse
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import FileSerializer
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from apps.common.validators import validate_uploaded_file
from apps.files.services.download_service import build_download_file
from apps.files.services.distributor import distribute_file

from .models import File
from apps.sharing.models import ShareLink



class FileUploadView(generics.CreateAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        uploaded_file = self.request.FILES["file"]

        validate_uploaded_file(
            uploaded_file
        )

        file_obj = serializer.save(
            owner=self.request.user,
            original_name=uploaded_file.name,
            file_size=uploaded_file.size,
        )

        distribute_file(
            file_obj
        )


class FileListView(generics.ListAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return File.objects.filter(
            owner=self.request.user
        ).order_by("-created_at")


class FileDetailView(generics.RetrieveAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return File.objects.filter(
            owner=self.request.user
        )


class FileDeleteView(generics.DestroyAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return File.objects.filter(
            owner=self.request.user
        )

    def perform_destroy(self, instance):
        if instance.file:
            instance.file.delete(save=False)

        instance.delete()


class FileDownloadView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        file_obj = File.objects.get(pk=pk)

        if file_obj.owner != request.user:
            raise PermissionDenied(
                "You do not own this file."
            )

        download_path = build_download_file(
            file_obj
        )

        return FileResponse(
            open(download_path, "rb"),
            as_attachment=True,
            filename=file_obj.original_name,
        )
    

class GuestUploadView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        uploaded_file = request.FILES.get("file")

        if not uploaded_file:
            return Response(
                {"error": "File is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        validate_uploaded_file(uploaded_file)

        expires_in_days = int(
            request.data.get(
                "expires_in_days",
                1
            )
        )

        max_downloads = int(
            request.data.get(
                "max_downloads",
                10
            )
        )

        password = request.data.get(
            "password"
        )

        delete_after = (
            timezone.now()
            + timedelta(days=expires_in_days)
        )

        file_obj = File.objects.create(
            owner=None,
            file=uploaded_file,
            original_name=uploaded_file.name,
            file_size=uploaded_file.size,
            is_temporary=True,
            delete_after=delete_after,
        )

        share_link = ShareLink.objects.create(
            file=file_obj,
            expires_at=delete_after,
            max_downloads=max_downloads,
            password_hash=(
                make_password(password)
                if password
                else None
            ),
        )

        return Response(
            {
                "token": str(
                    share_link.token
                )
            },
            status=status.HTTP_201_CREATED,
        )