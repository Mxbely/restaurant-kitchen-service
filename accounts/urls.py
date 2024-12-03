from django.urls import path
from django.urls import path, include

from .views import (
    CookListView,
    CookDetailView,
    CookCreateView,
    CookUpdateView,
    CookDeleteView,
    ChangePasswordView,
    RegisterView,
)

app_name = "accounts"

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("register/", RegisterView.as_view(), name="register"),
    path("cooks/", CookListView.as_view(), name="cook-list"),
    path("cooks/<int:pk>/", CookDetailView.as_view(), name="cook-detail"),
    path("cooks/create/", CookCreateView.as_view(), name="cook-create"),
    path("cooks/<int:pk>/update/", CookUpdateView.as_view(), name="cook-update"),
    path("cooks/<int:pk>/delete/", CookDeleteView.as_view(), name="cook-delete"),
    path(
        "cooks/<int:pk>/change-password/",
        ChangePasswordView.as_view(),
        name="change-password",
    ),
]
