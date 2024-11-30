
from django.urls import path
from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import register, CookListView, CookDetailView, CookCreateView, CookUpdateView, CookDeleteView

app_name = "accounts"

urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    path("", include("django.contrib.auth.urls")),
    path("register/", register, name="register"),
    path("cooks/", CookListView.as_view(), name="cook-list"),
    path("cooks/<int:pk>/", CookDetailView.as_view(), name="cook-detail"),
    path("cooks/create/", CookCreateView.as_view(), name="cook-create"),
    path("cooks/<int:pk>/update/", CookUpdateView.as_view(), name="cook-update"),
    path("cooks/<int:pk>/delete/", CookDeleteView.as_view(), name="cook-delete"),
]
