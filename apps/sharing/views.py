from datetime import timedelta
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.http import FileResponse
from django.utils import timezone

from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.files.models import File

from .models import ShareLink
from rest_framework import generics
from .serializers import ShareLinkSerializer

from apps.files.services.download_service import (
    build_download_file,
)


class CreateShareLinkView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        file_id = request.data.get("file_id")
        password = request.data.get("password")
        expires_in_days = int(
            request.data.get(
                "expires_in_days",
                7
            )
        )

        max_downloads = int(
            request.data.get(
                "max_downloads",
                10
            )
        )

        try:
            file_obj = File.objects.get(
                id=file_id,
                owner=request.user
            )
        except File.DoesNotExist:
            return Response(
                {
                    "error": "File not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        share_link = ShareLink.objects.create(
            file=file_obj,
            expires_at=timezone.now()
            + timedelta(days=expires_in_days),
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
            }
        )


class ShareLinkInfoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):

        try:
            share_link = ShareLink.objects.get(
                token=token
            )
        except ShareLink.DoesNotExist:
            return Response(
                {
                    "error": "Invalid link."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "filename": share_link.file.original_name,
                "size": share_link.file.file_size,
                "downloads": share_link.current_downloads,
                "expires_at": share_link.expires_at,
            }
        )


class ShareDownloadView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        share_link = ShareLink.objects.filter(token=token).select_related("file").first()

        if not share_link:
            return Response({"error": "Invalid link."}, status=404)

        if not share_link.is_active:
            return Response({"error": "Link disabled."}, status=400)

        if timezone.now() > share_link.expires_at:
            return Response({"error": "Link expired."}, status=400)

        if share_link.current_downloads >= share_link.max_downloads:
            return Response({"error": "Download limit reached."}, status=400)

        if share_link.password_hash:
            password = request.query_params.get("password")

            if not password:
                return Response({"error": "Password required."}, status=400)

            if not check_password(password, share_link.password_hash):
                return Response({"error": "Invalid password."}, status=400)

        share_link.current_downloads += 1
        share_link.save(update_fields=["current_downloads"])

        download_path = build_download_file(
            share_link.file
        )

        return FileResponse(
            open(download_path, "rb"),
            as_attachment=True,
            filename=share_link.file.original_name,
        )


class MyShareLinksView(generics.ListAPIView):
    serializer_class = ShareLinkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ShareLink.objects.filter(
            file__owner=self.request.user
        ).order_by("-created_at")
    
    
class RevokeShareLinkView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, token):

        try:
            share_link = ShareLink.objects.get(
                token=token,
                file__owner=request.user
            )
        except ShareLink.DoesNotExist:
            return Response(
                {
                    "error": "Link not found."
                },
                status=404
            )

        share_link.is_active = False
        share_link.save()

        return Response(
            {
                "message": "Link revoked."
            }
        )