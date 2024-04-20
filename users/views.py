from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse

from users.forms import LoginUserForm


def login_user(request: HttpRequest):
    match request.method:
        case 'POST':
            form = LoginUserForm(request.POST)
            if form.is_valid():
                user = authenticate(request,
                                    username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password']
                                    )
                if user and user.is_active:
                    a = login(request, user)
                    return HttpResponseRedirect(reverse('home'))

        case _:
            form = LoginUserForm()

    return render(request, 'users/login.html', {'form': form})


def logout_user(request: HttpRequest):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('users:login'))
