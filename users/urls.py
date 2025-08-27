from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)

from users.apps import UsersConfig
from users.views import (
    UserCreateAPIView, UserDestroyAPIView, UserListAPIView,
    UserRetrieveAPIView, UserUpdateAPIView
)

app_name = UsersConfig.name

urlpatterns = [
    path("users/", UserListAPIView.as_view(), name="users_list"),
    path("users/<int:pk>/", UserRetrieveAPIView.as_view(), name="user_detail"),
    path(
        "users/register/",
        UserCreateAPIView.as_view(permission_classes=(AllowAny,)),
        name="user_register",
    ),
    path(
        "users/delete/<int:pk>/",
        UserDestroyAPIView.as_view(),
        name="user_delete",
    ),
    path(
        "users/update/<int:pk>/",
        UserUpdateAPIView.as_view(),
        name="user_update",
    ),
    path(
        "users/login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "users/token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
]
