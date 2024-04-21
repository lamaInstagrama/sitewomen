from django.contrib.auth.views import LoginView
from users.forms import LoginUserForm


class LoginUser(LoginView):
    template_name = 'users/login.html'
    form_class = LoginUserForm
    extra_context = {'title': "Авторизация"}

    # def get_success_url(self):
    #     return reverse_lazy('about')
