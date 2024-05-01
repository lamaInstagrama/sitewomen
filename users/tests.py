from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy


class RegisterUserTestCase(TestCase):
    def setUp(self):
        self.data = {
            'username': 'user_1',
            'email': 'user1@sitewomen.ru',
            'first_name': 'Sergey',
            'last_name': 'Balakirev',
            'password1': '12345678Aa',
            'password2': '12345678Aa',
        }
        self.User = get_user_model()

    def test_form_registration(self):
        path = reverse_lazy('users:register')

        request = self.client.get(path=path)
        self.assertEqual(request.status_code, 200, 'Неверный код ответа')
        self.assertTemplateUsed(request, 'users/register.html',
                                msg_prefix='Неверный шаблон при подключении')

        request = self.client.post(path=path, data=self.data)
        self.assertEqual(request.status_code, 302, 'Неверный код ответа')
        self.assertRedirects(request, expected_url=reverse_lazy('users:login'),
                             msg_prefix='Не произошел редирект')
        self.assertTrue(self.User.objects.filter(username=self.data.get('username')).exists(),
                        msg='Пользователь не был создан')

    def test_form_registration_errors(self):
        path = reverse_lazy('users:register')
        self.client.post(path=path, data=self.data)
        request = self.client.post(path=path, data=self.data)
        self.assertContains(request, 'Пользователь с таким именем уже суще')

        self.data['password2'] = '1234'
        self.data['username'] = 'root123'
        request = self.client.post(path=path, data=self.data)
        self.assertContains(request, 'Введенные пароли не совпадают.', html=True)

