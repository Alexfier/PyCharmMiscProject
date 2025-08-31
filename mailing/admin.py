from django.contrib import admin

from mailing.models import Mailing, Message, Recipient


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email")
    search_fields = ('full_name', 'email')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("topic",)
    ordering = ("topic",)
    search_fields = ("topic", "text")


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("id", "end_sending", "status")
    ordering = ("id",)
    search_fields = ("status", "mes")
