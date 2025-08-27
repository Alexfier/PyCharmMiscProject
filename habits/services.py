import requests

from config.settings import TELEGRAM_TOKEN


def send_tg_message(chat_id, message):
    """Отправка сообщения в чат Telegram"""

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
        "disable_notification": False,
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return True
    except Exception as e:
        print("Error: ", e)
        return False


def prepare_habit_message(habit):
    """Формирование сообщения о привычке"""
    message = (
        f"⏰ <b>Напоминание о привычке</b>\n\n"
        f"<b>Действие:</b> {habit.action}\n"
        f"<b>Место:</b> {habit.place}\n"
        f"<b>Время на выполнение:</b> {habit.duration} сек.\n"
    )

    if habit.related_habit:
        message += f"<b>Связанная привычка:</b> {habit.related_habit.action}\n"
    elif habit.reward:
        message += f"<b>Вознаграждение:</b> {habit.reward}\n"

    return message
