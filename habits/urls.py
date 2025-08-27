from django.urls import path
from rest_framework.routers import DefaultRouter

from habits.apps import HabitsConfig
from habits.views import HabitPublicListAPIView, HabitViewSet

app_name = HabitsConfig.name

router = DefaultRouter()
router.register(r"habits", HabitViewSet, basename="habits")

urlpatterns = [
    path(
        "habits/public/",
        HabitPublicListAPIView.as_view(),
        name="public_habits",
    ),
] + router.urls
