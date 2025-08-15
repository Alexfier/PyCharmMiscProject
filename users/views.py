from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.core.checks import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView


from users.forms import RegisterForm, LoginForm, ProfileForm
from users.models import User, Profile
from django.views.generic import ListView


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("messaging:mailing_list")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("messaging:mailing_list")


class LoginView(LoginView):
    form_class = LoginForm
    template_name = "users/login.html"

    def get_success_url(self):
        return reverse_lazy("messaging:mailing_list")


def logout_view(request):
    logout(request)
    return redirect("messaging:mailing_list")


class ProfileView(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "users/profile.html"

    def get_object(self, queryset=None):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def get_success_url(self):
        return reverse_lazy("users:profile")


class CustomPasswordResetView(PasswordResetView):
    template_name = "users/password_reset_form.html"
    email_template_name = "users/password_reset_email.html"
    subject_template_name = "users/password_reset_subject.txt"
    success_url = "/users/password_reset/done/"


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "users/password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html"
    success_url = "/users/reset/done/"


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "users/password_reset_complete.html"


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "messaging/user_list.html"
    context_object_name = "users"


class ToggleUserStatusView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Контроллер для блокировки/разблокировки пользователей"""

    def test_func(self):
        # Проверяем права на блокировку пользователей
        return self.request.user.has_perm("users.can_block_user")

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.is_active = not user.is_active
        user.save()

        action = "разблокирован" if user.is_active else "заблокирован"
        messages.success(request, f"Пользователь {user.email} успешно {action}")

        return redirect("messaging:user_list")
