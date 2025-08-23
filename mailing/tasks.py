import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from mailing.models import Mailing, MailingAttempt

logger = logging.getLogger(__name__)


@shared_task(bind=True, retry_backoff=True)
def send_mailing_task(self, mailing_id):
    """
    Рассылает электронные письма клиентам из списка рассылки.
    """
    mailing = Mailing.objects.get(pk=mailing_id)

    # Проверяем время отправки
    if mailing.status == "completed":
        logger.info(f"Mailing {mailing.pk} is already completed.")
        return

    # Привлекаем клиентов для рассылки
    clients = mailing.clients.all()

    for client in clients:
        try:
            send_mail(
                mailing.message.subject,
                mailing.message.body,
                settings.EMAIL_HOST_USER,  # Отправляем письмо
                [client.email],  # Электронное письмо получателя
                fail_silently=False,
            )
            # Запишите успешную попытку
            MailingAttempt.objects.create(
                mailing=mailing,
                status="success",
                server_response="Email sent successfully",
            )
            logger.info(f"Sent email to {client.email} for mailing {mailing.pk}")

        except Exception as e:
            # Запишите неудачную попытку
            MailingAttempt.objects.create(
                mailing=mailing, status="failure", server_response=str(e)
            )
            logger.error(
                f"Failed to send email to {client.email} for mailing {mailing.pk}: {e}"
            )
            raise self.retry(exc=e, countdown=60)  # Повторите попытку через 60 секунд

    # При необходимости обновите статус рассылки
    mailing.status = "completed"
    mailing.save()
    logger.info(f"Mailing {mailing.pk} completed.")


@shared_task(bind=False)  #  bind=False - КЛЮЧЕВОЙ МОМЕНТ
def schedule_mailing_wrapper(mailing_id):
    """Запускает задачу отправки рассылки асинхронно через Celery."""
    send_mailing_task.delay(mailing_id)  # или apply_async, если нужно больше контроля