from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Модель пользователя
    """

    id: models.AutoField
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(
        max_length=35,
        verbose_name="Телефон",
        blank=True,
        null=True,
    )
    city = models.CharField(
        max_length=65,
        verbose_name="Город",
        blank=True,
        null=True,
    )
    chat_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="ID чата Telegram",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
