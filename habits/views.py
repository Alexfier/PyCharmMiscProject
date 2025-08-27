from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.serializers import HabitSerializer
from users.permissions import IsAdminUser, IsOwner, IsSuperUser


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator
    queryset = Habit.objects.all()
    permission_classes = (
        IsAuthenticated,
        (IsSuperUser | IsAdminUser | IsOwner),
    )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return Habit.objects.filter(
            owner=self.request.user,
            is_active=True,
        )

    def perform_destroy(self, instance):
        if self.request.user.is_staff:
            instance.delete()
        else:
            instance.is_active = False
            instance.save(update_fields=["is_active"])


class HabitPublicListAPIView(ListAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_public=True)
    pagination_class = HabitPaginator
