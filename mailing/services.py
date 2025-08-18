from django.core.cache import cache

from config.settings import CACHE_ENABLED
from mailing.models import Mailing, Message, Recipient


def get_all_recipients():
    if CACHE_ENABLED:
        recipients = cache.get("recipients")
        if recipients is None:
            recipients = Recipient.objects.all()
            cache.set("recipients", recipients, 120)
        else:
            recipients = Recipient.objects.all()

        return recipients


def get_all_messages():
    if CACHE_ENABLED:
        messages = cache.get("messages")
        if messages is None:
            messages = Message.objects.all()
            cache.set("messages", messages, 120)
        else:
            messages = Message.objects.all()

        return messages


def get_all_mailing():
    if CACHE_ENABLED:
        mailing = cache.get("mailing")
        if mailing is None:
            mailing = Mailing.objects.all()
            cache.set("mailing", mailing, 120)
        else:
            mailing = Mailing.objects.all()

        return mailing
