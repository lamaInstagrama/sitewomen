from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm


class LoginUser(LoginView):
    template_name = 'users/login.html'
    form_class = LoginUserForm
    extra_context = {'title': "Авторизация"}

    # def get_success_url(self):
    #     return reverse_lazy('about')


class RegisterUser(CreateView):
    template_name = 'users/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('users:login')
    extra_context = {'title': 'Регистрация'}


class ProfileUser(LoginRequiredMixin, UpdateView):
    template_name = 'users/profile.html'
    extra_context = {'title': 'Профиль', 'default_photo': settings.DEFAULT_USER_PHOTO}
    form_class = ProfileUserForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('users:profile')


class UserChangePassword(PasswordChangeView):
    template_name = 'users/password_change_form.html'
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")

