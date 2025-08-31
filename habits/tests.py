from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from habits.models import Habit
from users.models import User


class HabitTests(APITestCase):
    """Тестирование модели Habit"""

    def setUp(self):
        """Подготовка данных для тестирования"""
        self.client = APIClient()
        self.user = User.objects.create(
            email="user@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        self.admin = User.objects.create(
            email="admin@example.com",
            password="adminpass123",
            first_name="Admin",
            last_name="User",
            is_staff=True,
        )

        self.habit = Habit.objects.create(
            owner=self.user,
            place="Дома",
            time_action="08:00:00",
            action="Чтение книги",
            duration=60,
            periodicity=1,
            is_public=False,
        )

        self.public_habit = Habit.objects.create(
            owner=self.admin,
            place="Парк",
            time_action="18:00:00",
            action="Прогулка",
            duration=30,
            periodicity=2,
            is_public=True,
        )

        self.pleasant_habit = Habit.objects.create(
            owner=self.admin,
            place="Парк",
            time_action="18:00:00",
            action="Прогулка",
            duration=30,
            is_pleasant_habit=True,
            periodicity=2,
            is_public=False,
        )

    def test_create_habit(self):
        """Тест создания привычки"""
        self.client.force_authenticate(user=self.user)
        url = reverse("habits:habits-list")
        data = {
            "place": "Офис",
            "time_action": "12:00:00",
            "action": "Обеденный перерыв",
            "duration": 15,
            "periodicity": 1,
            "is_public": False,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 4)
        self.assertEqual(Habit.objects.last().owner, self.user)

    def test_get_user_habits(self):
        """Тест получения списка привычек пользователя"""
        self.client.force_authenticate(user=self.user)
        url = reverse("habits:habits-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["action"], "Чтение книги")

    def test_get_public_habits(self):
        """Тест получения публичных привычек"""
        self.client.force_authenticate(user=self.user)
        url = reverse("habits:public_habits")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["action"], "Прогулка")

    def test_update_habit(self):
        """Тест обновления привычки"""
        self.client.force_authenticate(user=self.user)
        url = reverse("habits:habits-detail", args=[self.habit.id])
        data = {"action": "Чтение научной литературы"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.action, "Чтение научной литературы")

    def test_delete_habit_by_owner(self):
        """Тест деактивации привычки владельцем"""
        self.client.force_authenticate(user=self.user)
        url = reverse("habits:habits-detail", args=[self.habit.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.habit.refresh_from_db()
        self.assertFalse(self.habit.is_active)

    def test_delete_habit_by_admin(self):
        """Тест полного удаления привычки админом"""
        self.client.force_authenticate(user=self.admin)
        url = reverse("habits:habits-detail", args=[self.habit.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(id=self.habit.id).exists())

    def test_habit_validation_duration(self):
        """Тест валидации модели привычки по продолжительности выполнения"""
        invalid_habit = Habit(
            owner=self.user,
            place="Дома",
            time_action="08:00:00",
            action="Просмотр ТВ",
            duration=121,
            periodicity=1,
        )

        with self.assertRaises(Exception) as context:
            invalid_habit.full_clean()
        self.assertIn(
            "Время выполнения не должно превышать 120 секунд",
            str(context.exception),
        )

    def test_habit_validation_periodicity(self):
        """Тест валидации модели привычки по периодичности"""
        invalid_habit = Habit(
            owner=self.user,
            place="Дома",
            time_action="08:00:00",
            action="Просмотр ТВ",
            duration=120,
            periodicity=8,
        )

        with self.assertRaises(Exception) as context:
            invalid_habit.full_clean()
        self.assertIn(
            "Нельзя выполнять привычку реже, " "чем 1 раз в 7 дней",
            str(context.exception),
        )

    def test_pleasant_habit_validation_reward(self):
        """Тест валидации приятной привычки и вознаграждения"""
        pleasant_habit = Habit(
            owner=self.user,
            place="Диван",
            time_action="20:00:00",
            action="Просмотр кино",
            is_pleasant_habit=True,
            reward="Чай",
            duration=30,
            periodicity=1,
        )

        with self.assertRaises(Exception) as context:
            pleasant_habit.full_clean()
        self.assertIn(
            "Приятная привычка не может иметь вознаграждения",
            str(context.exception),
        )

    def test_related_and_reward_habit_validation(self):
        """Тест валидации связанной привычки и вознаграждения"""
        pleasant_habit = Habit(
            owner=self.user,
            place="Диван",
            time_action="20:00:00",
            action="Просмотр кино",
            related_habit=self.pleasant_habit,
            is_pleasant_habit=False,
            reward="Чай",
            duration=30,
            periodicity=1,
        )

        with self.assertRaises(Exception) as context:
            pleasant_habit.full_clean()
        self.assertIn(
            "Можно указать либо связанную привычку,"
            " либо вознаграждение, но не оба",
            str(context.exception),
        )

    def test_related_pleasant_habit_validation(self):
        """Тест валидации связанной приятной привычки"""
        pleasant_habit = Habit(
            owner=self.user,
            place="Диван",
            time_action="20:00:00",
            action="Просмотр кино",
            related_habit=self.habit,
            is_pleasant_habit=False,
            duration=30,
            periodicity=1,
        )

        with self.assertRaises(Exception) as context:
            pleasant_habit.full_clean()
        self.assertIn(
            "Связанная привычка должна быть приятной", str(context.exception)
        )

    def test_habit_string_representation(self):
        """Тест строкового представления привычки"""
        self.assertEqual(str(self.habit), "Чтение книги")

    def test_pagination(self):
        """Тест пагинации"""
        for i in range(10):
            Habit.objects.create(
                owner=self.user,
                place=f"Место {i}",
                time_action="08:00:00",
                action=f"Действие {i}",
                duration=30,
                periodicity=1,
            )

        self.client.force_authenticate(user=self.user)
        url = reverse("habits:habits-list") + "?page=2&page_size=5"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 5)
        self.assertIn("page=3", response.data["next"])

    def test_unauthorized_access(self):
        """Тест доступа без авторизации"""
        url = reverse("habits:habits-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
