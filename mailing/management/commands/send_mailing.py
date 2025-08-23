from django.core.mail import send_mail
from django.core.management import BaseCommand

from config.settings import EMAIL_HOST_USER
from mailing.models import AttemptSending, Mailing


class Command(BaseCommand):
    def handle(self):

        def send_mailing():
            mailings = Mailing.objects.filter(status__in=("created", "launched"))
            for mailing in mailings:

                if mailing.enabled is True:

                    recipients = mailing.recipients.all()

                    for recipient in recipients:
                        try:
                            send_mail(mailing.message.topic, mailing.message.text, EMAIL_HOST_USER, [recipient.email])

                            AttemptSending.objects.create(mailing=mailing, status="success",
                                                          response="Сообщение отправлено успешно")

                        except Exception as e:
                            AttemptSending.objects.create(mailing=mailing, status="not_success", response=str(e))

                    mailing.status = "launched"
                    mailing.save()

        send_mailing()
