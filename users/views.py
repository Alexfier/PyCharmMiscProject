from rest_framework.generics import (
    CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
)
from rest_framework.permissions import IsAuthenticated

from users.models import User
from users.permissions import IsAdminUser, IsOwner, IsSuperUser
from users.serializers import UserAdminSerializer, UserSerializer


class UserListAPIView(ListAPIView):
    serializer_class = UserAdminSerializer
    permission_classes = [IsAuthenticated, IsSuperUser | IsAdminUser]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(is_superuser=False)


class UserRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsSuperUser | IsAdminUser | IsOwner]
    lookup_field = "pk"

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return UserAdminSerializer
        return UserSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(is_superuser=False)


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsSuperUser | IsAdminUser | IsOwner]

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return UserAdminSerializer
        return UserSerializer

    def perform_update(self, serializer):
        if "password" in serializer.validated_data:
            user = serializer.save()
            user.set_password(serializer.validated_data["password"])
            user.save()
        else:
            serializer.save()


class UserDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsSuperUser | IsAdminUser]
    serializer_class = UserAdminSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(is_superuser=False)
