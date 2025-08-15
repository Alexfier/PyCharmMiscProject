from celery import shared_task
from .models import Mailing
from django.core.mail import send_mail


@shared_task
def send_mailing_async(mailing_id):
    try:
        mailing = Mailing.objects.get(id=mailing_id)
    except Mailing.DoesNotExist:
        return

    messages = mailing.messages.all()
    recipients = mailing.recipients.all()

    def send_message(email, text):
        send_mail(
            subject="Новое сообщение",
            message=text,
            from_email="ekaterina.kuz@gmail.com",
            recipient_list=[email],
            fail_silently=False,
        )

    for message in messages:
        for recipient in recipients:
            email = recipient.email
            if email:  # Проверка наличия email
                send_message(email, message.text)

    mailing.status = Mailing.Status.COMPLETED
    mailing.save()
