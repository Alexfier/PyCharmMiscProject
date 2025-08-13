import secrets
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForms
from users.models import User
import secrets


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForms
    success_url = reverse_lazy('messagin_service:home')

    # def form_valid(self, form):
    #     user = form.save()
    #     self.send_welcome_email(user.email)
    #     return super().form_valid(form)
    #
    # def send_welcome_email(self, user_email):
    #     subject = 'Добро пожаловать в наш сервис'
    #     message = 'Спасибо, что зарегистрировались в нашем сервисе!'
    #     from_email = 'feat9999@yandex.ru'
    #     recipient_list = [user_email]
    #     send_mail(subject, message, from_email, recipient_list)

    def form_invalid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject='Подтверждение почты',
            message=f'Перейдите по ссылке для подтверждения регистрации {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:home'))
