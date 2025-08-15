from django.core.management.base import BaseCommand
from django.utils import timezone
from messaging.models import Mailing
from messaging.tasks import send_mailing


class Command(BaseCommand):
    help = "Send scheduled messages"

    def handle(self, *args, **options):
        now = timezone.now()

        mailings = Mailing.objects.filter(
            start_time__lte=now, status=Mailing.CREATED, is_active=True
        ).exclude(end_time__lt=now)

        count = 0

        for mailing in mailings:
            try:
                mailing.status = Mailing.STARTED
                mailing.save()
                send_mailing.delay(mailing.id)
                count += 1

                self.stdout.write(f"Started mailing ID {mailing.id}")
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Error starting mailing ID {mailing.id}: {str(e)}"
                    )
                )

        self.stdout.write(self.style.SUCCESS(f"Successfully started {count} mailings"))
