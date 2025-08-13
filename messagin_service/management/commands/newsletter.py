# from django.core.mail import send_mail
# from django.core.management.base import BaseCommand
# from django.utils import timezone
# from messagin_service.models import Mailings, Attempt, Recipient
#
#
# class Command(BaseCommand):
#     help = 'Send newsletters to users'
#
#     def handle(self, *args, **kwargs):
#         newsletters = Mailings.objects.filter(active=True)
#
#         emails = Recipient.objects.values_list('email', flat=True)
#         for newsletter in newsletters:
#             try:
#                 send_mail(
#                     'test message subject',
#                     'test message',
#                     'feat9999@yandex.ru',
#                     list(emails),
#                 fail_silently=False,)
#
#                 Attempt.objects.create(status='Успешно', server_response='OK', newsletter=newsletter)
#             except Exception as e:
#                 Attempt.objects.create(status='Не успешно', server_response=str(e), newsletter=newsletter)

                # # Сохраняем попытку рассылки
                # Attempt.objects.create(
                #     attempt_time=attempt_time.now(),
                #     status=status,
                #     server_response=response,
                #     newsletter=newsletter
                # )
                # self.stdout.write(self.style.SUCCESS(f'{status}: {newsletter.title}'))