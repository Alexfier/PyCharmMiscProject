from django.contrib import admin
from .models import Client, Message, Mailing, Attempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "full_name", "comment")
    search_fields = ("email", "full_name")
    list_filter = ("comment",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "body_preview")
    search_fields = ("subject", "body")

    def body_preview(self, obj):
        return f"{obj.body[:50]}..." if len(obj.body) > 50 else obj.body

    body_preview.short_description = "Превью тела письма"


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("id", "start_time", "status", "message_subject", "clients_count")
    search_fields = ("status", "message__subject")
    list_filter = ("status", "start_time")
    filter_horizontal = ("clients",)

    def message_subject(self, obj):
        return obj.message.subject

    message_subject.short_description = "Тема письма"

    def clients_count(self, obj):
        return obj.clients.count()

    clients_count.short_description = "Кол-во получателей"


@admin.register(Attempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "mailing_info",
        "attempt_time",
        "status",
        "server_response_preview",
    )
    search_fields = ("status", "server_response", "mailing__message__subject")
    list_filter = ("status", "attempt_time")

    def mailing_info(self, obj):
        return f"Рассылка #{obj.mailing.id} ({obj.mailing.message.subject})"

    mailing_info.short_description = "Рассылка"

    def server_response_preview(self, obj):
        return f"{obj.server_response[:50]}..." if obj.server_response else ""

    server_response_preview.short_description = "Ответ сервера"
