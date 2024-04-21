from django.contrib.auth.views import LoginView
from django.shortcuts import render

from users.forms import LoginUserForm, RegisterUserForm


class LoginUser(LoginView):
    template_name = 'users/login.html'
    form_class = LoginUserForm
    extra_context = {'title': "Авторизация"}

    # def get_success_url(self):
    #     return reverse_lazy('about')


def register(request):
    match request.method:
        case 'POST':
            form = RegisterUserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)  # создание объекта без сохранения в БД
                user.set_password(form.cleaned_data.get('password'))
                user.save()
                return render(request, 'users/register_done.html')

        case _:
            form = RegisterUserForm()

    return render(request, 'users/register.html', {'form': form, 'title': 'Регистрация'})
