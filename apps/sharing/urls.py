from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.CreateShareLinkView.as_view()),
    path("my-links/", views.MyShareLinksView.as_view()),
    path("<uuid:token>/download/", views.ShareDownloadView.as_view()),
    path("<uuid:token>/revoke/", views.RevokeShareLinkView.as_view()),
    path("<uuid:token>/", views.ShareLinkInfoView.as_view()),
]