from django.contrib import admin
from messagin_service.models import Recipient, Message, Mailings


@admin.register(Recipient)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "full_name", "comment")
    search_fields = ("email", "full_name")
    list_filter = ("comment",)
