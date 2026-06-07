from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.files.models import File
from apps.sharing.models import ShareLink


class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_files = File.objects.filter(owner=request.user).count()
        total_shares = ShareLink.objects.filter(file__owner=request.user).count()
        active_shares = ShareLink.objects.filter(file__owner=request.user, is_active=True,).count()

        return Response(
            {
                "total_files": total_files,
                "total_shares": total_shares,
                "active_shares": active_shares,
            }
        )