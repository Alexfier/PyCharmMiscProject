from django.db import models

class Recipient(models.Model):
    email = models.EmailField(unique=True, verbose_name='Email')
    full_name = models.CharField(max_length=100, help_text='Введите свое Ф.И.О')
    comment = models.TextField(verbose_name='Комментарий', blank=True, null=True)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return self.full_name


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Тело письма")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return self.subject


class Mailings(models.Model):
    STATUS_CHOICES = [
        ('CREATED', 'Создана'),
        ('STARTED', 'Запущена'),
        ('FINISHED', 'Завершена'),
    ]

    date_first = models.DateTimeField(verbose_name='Дата и время первой отправки ')#auto_now_add=True)
    date_end = models.DateTimeField(verbose_name='Дата и время окончания отправки', null=True, blank=True)#auto_now=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,
        default='CREATED', verbose_name='Статус')
    message = models.ForeignKey('Message', on_delete=models.CASCADE)
    recipient = models.ManyToManyField(Recipient)

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"


class Attempt(models.Model):
    STATUS_CHOICES = [
        ('SUCCESS', "Успешно"),
        ('FAILURE', "Неуспешно"),
    ]

    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name="Время попытки")
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, verbose_name="Статус попытки")
    server_response = models.TextField(
        blank=True, null=True, verbose_name="Ответ сервера")
    mailing = models.ForeignKey(
        Mailings, on_delete=models.CASCADE, verbose_name="Рассылка")

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
