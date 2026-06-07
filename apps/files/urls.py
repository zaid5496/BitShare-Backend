from django.urls import path
from . import views



urlpatterns = [
    path("upload/", views.FileUploadView.as_view(),),
    path("", views.FileListView.as_view(),),
    path("<int:pk>/", views.FileDetailView.as_view(),),
    path("<int:pk>/delete/", views.FileDeleteView.as_view(),),
    path("<int:pk>/download/", views.FileDownloadView.as_view(),),
    path("guest/upload/", views.GuestUploadView.as_view(),),
]