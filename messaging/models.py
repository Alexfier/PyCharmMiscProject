from django.core.mail import send_mail
from django.db import models
from django.utils import timezone

from config import settings
from users.models import User


class Client(models.Model):
    email = models.EmailField(verbose_name="Email")
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Владелец", null=True
    )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        permissions = [
            ("can_view_client", "Can view client"),
            ("can_block_client", "Can block client"),
        ]

    def __str__(self):
        return self.full_name


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Тело письма")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Владелец", null=True
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        permissions = [
            ("can_view_message", "Can view message"),
            ("can_disable_message", "Can disable message"),
        ]

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

    FREQUENCY_CHOICES = [
        (DAILY, "Ежедневная"),
        (WEEKLY, "Еженедельная"),
        (MONTHLY, "Ежемесячная"),
    ]

    CREATED = "created"
    STARTED = "started"
    COMPLETED = "completed"

    STATUS_CHOICES = [
        (CREATED, "Создана"),
        (STARTED, "Запущена"),
        (COMPLETED, "Завершена"),
    ]

    start_time = models.DateTimeField(verbose_name="Время начала рассылки")
    end_time = models.DateTimeField(
        verbose_name="Время окончания рассылки", null=True, blank=True
    )
    frequency = models.CharField(
        max_length=100, default="weekly", verbose_name="Периодичность"
    )
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default=CREATED, verbose_name="Статус"
    )
    clients = models.ManyToManyField(Client, verbose_name="Клиенты")
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, verbose_name="Сообщение"
    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Владелец", null=True
    )
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [
            ("can_block_user", "Can block users"),
            ("can_view_all", "Can view all mailings"),
            ("can_finish_mailing", "Can finish any mailing"),
        ]

    def send(self):
        """Метод для отправки рассылки всем клиентам"""
        if self.status != self.CREATED:
            raise ValueError(
                "Рассылка может быть отправлена только в статусе 'Создана'"
            )
        if not self.is_active:
            raise ValueError("Нельзя отправить неактивную рассылку")
        if timezone.now() < self.start_time:
            raise ValueError("Время начала рассылки еще не наступило")
        if self.end_time and timezone.now() > self.end_time:
            raise ValueError("Время окончания рассылки уже прошло")

        # Получаем всех клиентов рассылки
        clients = self.clients.all()
        if not clients:
            raise ValueError("Нет клиентов для отправки")

        # Подготавливаем сообщение
        subject = self.message.subject
        message = self.message.body
        from_email = settings.DEFAULT_FROM_EMAIL

        # Отправляем каждому клиенту
        for client in clients:
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=from_email,
                    recipient_list=[client.email],
                    fail_silently=False,
                )

            except Exception as e:
                print(f"Ошибка при отправке клиенту {client.email}: {str(e)}")
                continue

        # Обновляем статус рассылки
        self.status = self.COMPLETED
        self.save()

        return len(clients)

    def __str__(self):
        return f"Рассылка {self.id} - {self.get_status_display()}"


class Attempt(models.Model):
    SUCCESS = "success"
    FAILURE = "failure"

    STATUS_CHOICES = [
        (SUCCESS, "Успешно"),
        (FAILURE, "Неуспешно"),
    ]

    mailing = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, verbose_name="Рассылка"
    )
    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name="Время попытки")
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, verbose_name="Статус попытки"
    )
    server_response = models.TextField(
        blank=True, null=True, verbose_name="Ответ сервера"
    )

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"

    def __str__(self):
        return f"Попытка {self.id} - {self.get_status_display()}"
