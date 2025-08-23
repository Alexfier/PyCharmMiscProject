from django.db import models

from users.models import User


class Recipient(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email", help_text="Введите электронную почту")
    full_name = models.CharField(max_length=150, verbose_name="ФИО", help_text="Введите ФИО")
    comment = models.TextField(verbose_name="Комментарий", help_text="Напишите комментарий", blank=True, null=True)

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Владелец", blank=True, null=True,
                              related_name="recipients")

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
        ordering = ["email"]


class Message(models.Model):
    topic = models.CharField(max_length=150, verbose_name="Тема сообщения", help_text="Введите тему сообщения")
    text = models.TextField(verbose_name="Текст сообщения", help_text="Напишите сообщение")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Владелец", blank=True, null=True,
                              related_name="messages")

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["topic"]


class Mailing(models.Model):
    first_sending = models.DateTimeField(verbose_name="Начало рассылки", blank=True, null=True)
    end_sending = models.DateTimeField(verbose_name="Дата окончания рассылки", blank=True, null=True)

    STATUS_OF_MAILING = [
        ("created", "Создана"),
        ("launched", "Запущена"),
        ("completed", "Завершена"),
    ]
    status = models.CharField(choices=STATUS_OF_MAILING, default='created', verbose_name="Статус рассылки",
                              help_text="Выберите статус рассылки")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="Сообщение",
                                help_text="Выберите сообщение")
    recipients = models.ManyToManyField(Recipient, verbose_name="Получатели", help_text="Выберите получателей")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Владелец рассылки", blank=True, null=True,
                              related_name="mailings")

    def __str__(self):
        return f"Рассылка №{self.pk}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["status"]
        permissions = [
            ("can_disabling_mailing", "Can disabling mailing"),
        ]


class AttemptSending(models.Model):
    time = models.DateTimeField(verbose_name="Дата и время попытки", auto_now_add=True)

    STATUS_OF_ATTEMPT = [
        ('success', 'Успешно'),
        ('not_success', 'Не успешно'),
    ]
    status = models.CharField(choices=STATUS_OF_ATTEMPT, default='not_success', verbose_name="Статус попытки")
    response = models.TextField(verbose_name="Ответ почтового сервера", null=True, blank=True)
    mailing = models.ForeignKey(Mailing, on_delete=models.SET_NULL, verbose_name="Рассылка", null=True, blank=True,
                                related_name="attempts")

    def __str__(self):
        return f'Попытка №{self.pk}'

    class Meta:
        verbose_name = "Попытка"
        verbose_name_plural = "Попытки"
        ordering = ["time"]
