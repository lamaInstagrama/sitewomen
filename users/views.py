from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import LoginUserForm, RegisterUserForm


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
