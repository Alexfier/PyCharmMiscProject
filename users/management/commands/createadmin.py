import os

from django.core.management.base import BaseCommand
from dotenv import load_dotenv

from users.models import User

load_dotenv(override=True)


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            user = User.objects.create(
                email=os.getenv("SUPERUSER_EMAIL"),
            )

            user.set_password(os.getenv("SUPERUSER_PASSWORD"))

            user.is_active = True
            user.is_staff = True
            user.is_superuser = True

            user.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Успешно создан супер-пользователь "
                    f"с электронной почтой {user.email}!"
                )
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"{e}"))
