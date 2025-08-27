from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from habits.services import prepare_habit_message, send_tg_message


@shared_task
def send_daily_habit_reminders():
    """Ежедневная отправка напоминаний о привычках"""
    now = timezone.localtime(timezone.now())
    current_time = now.time()

    habits = Habit.objects.filter(
        time_action__hour=current_time.hour,
        time_action__minute=current_time.minute,
        is_active=True,
        owner__isnull=False,
        owner__chat_id__isnull=False,
    ).select_related("owner", "related_habit")

    for habit in habits:
        message = prepare_habit_message(habit)
        if send_tg_message(habit.owner.chat_id, message):
            print(f"Sent reminder for habit {habit.id} to {habit.owner.email}")
        else:
            print(f"Failed to send reminder for habit {habit.id}")
