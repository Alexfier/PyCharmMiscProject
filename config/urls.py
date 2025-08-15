from django.urls import path, include
from django.views.generic.base import RedirectView
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("messaging.urls", namespace="messaging")),
    path("users/", include("users.urls", namespace="users")),
]
