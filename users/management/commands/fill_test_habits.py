import random
from datetime import time

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

from habits.models import Habit

User = get_user_model()
fake = Faker("ru_RU")


class Command(BaseCommand):
    help = "Заполняет базу тестовыми привычками (14 записей)"

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            email="testuser@example.com",
            defaults={
                "first_name": "Тестовый",
                "last_name": "Пользователь",
                "is_active": True,
            },
        )
        if created:
            user.set_password("Password2025")
            user.save()
        pleasant_habits = []

        for i in range(1, 15):
            is_pleasant = random.choice([True, False])

            habit = Habit.objects.create(
                owner=user,
                place=fake.city(),
                time_action=time(
                    hour=random.randint(6, 22), minute=random.randint(0, 59)
                ),
                action=fake.sentence(nb_words=3),
                is_pleasant_habit=is_pleasant,
                periodicity=random.randint(1, 7),
                reward=None if is_pleasant else fake.word(),
                duration=random.randint(30, 120),
                is_public=random.choice([True, False]),
                is_active=True,
            )

            if is_pleasant:
                pleasant_habits.append(habit)

            self.stdout.write(
                self.style.SUCCESS(f"Создана привычка {i}: {habit.action}")
            )

        normal_habits = Habit.objects.filter(is_pleasant_habit=False)
        for habit in normal_habits[:5]:
            if pleasant_habits:
                habit.related_habit = random.choice(pleasant_habits)
                habit.reward = None
                habit.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Связали привычку "{habit.action}" '
                        f'с приятной привычкой "{habit.related_habit.action}"'
                    )
                )

        self.stdout.write(
            self.style.SUCCESS("Успешно создано 14 тестовых привычек")
        )
