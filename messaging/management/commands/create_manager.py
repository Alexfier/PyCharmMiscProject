from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from messaging.models import Mailing, Client, Message

User = get_user_model()


class Command(BaseCommand):
    help = "Настройка ролей и прав доступа для сервиса рассылок"

    def handle(self, *args, **options):
        try:
            user_content_type = ContentType.objects.get_for_model(User)
        except ContentType.DoesNotExist:
            self.stdout.write(self.style.ERROR("ContentType для модели User не найден"))
            return

        # Создаем группы
        user_group, _ = Group.objects.get_or_create(name="Пользователи")
        manager_group, _ = Group.objects.get_or_create(name="Менеджеры")

        # Настраиваем права
        self.setup_user_permissions(user_group)
        self.setup_manager_permissions(manager_group, user_content_type)

        self.stdout.write(self.style.SUCCESS("Права доступа успешно настроены"))

    def setup_manager_permissions(self, group, user_content_type):
        """Настройка прав для менеджеров"""
        # Права для моделей рассылок
        for model in [Client, Mailing, Message]:
            content_type = ContentType.objects.get_for_model(model)
            permissions = Permission.objects.filter(content_type=content_type)
            group.permissions.add(*permissions)

        # Права для модели User
        user_permissions = Permission.objects.filter(content_type=user_content_type)
        group.permissions.add(*user_permissions)

        # Кастомные права
        custom_perms = [
            ("users", "can_block_user"),
            ("users", "can_view_all"),
            ("messaging", "can_finish_mailing"),
        ]

        for app_label, codename in custom_perms:
            try:
                perm = Permission.objects.get(
                    content_type__app_label=app_label, codename=codename
                )
                group.permissions.add(perm)
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f"Право {app_label}.{codename} не найдено. "
                        "Убедитесь, что оно объявлено в модели."
                    )
                )

    def setup_user_permissions(self, group):
        """Настройка базовых прав для пользователей"""
        for model in [Client, Mailing, Message]:
            content_type = ContentType.objects.get_for_model(model)
            permissions = Permission.objects.filter(content_type=content_type).exclude(
                codename__startswith="delete"
            )
            group.permissions.add(*permissions)
