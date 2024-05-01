from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.test import TestCase
from django.urls import reverse_lazy

from women.models import Women
from women.views import WomenHome


class GetPagesTestCase(TestCase):
    fixtures = 'sitewomen_db.json',

    def test_home_page(self):
        paginator = Paginator(Women.published.all(), WomenHome.paginate_by)
        for page_num in paginator.page_range:
            path = f'{reverse_lazy('home')}?page={page_num}'
            response = self.client.get(path=path)
            p = paginator.get_page(page_num)

            self.assertEqual(response.status_code, 200, 'Неверный статус')
            self.assertTemplateUsed(response, 'women/index.html', 'Использован неверный шаблон')
            self.assertEqual(response.context_data.get('title'), 'Главная страница', 'Неверный заголовок')
            self.assertQuerysetEqual(response.context_data.get('posts'), p.object_list)

    def test_add_page(self):
        self.client.login(username='root', password='1234')
        path = reverse_lazy('add_page')
        request = self.client.get(path)

        self.assertEqual(request.status_code, 200, 'Неверный код ответа')
        self.assertEqual(request.context_data.get('title'), 'Добавление статьи', 'Неверный заголовок')


class RedirectPagesTestCase(TestCase):
    def test_add_page_redirect(self):
        path = reverse_lazy('add_page')
        redirect_url = f'{reverse_lazy('users:login')}?next={path}'
        response = self.client.get(path=path)

        self.assertEqual(response.status_code, 302, 'Неверный код ответа')
        self.assertRedirects(response, redirect_url, msg_prefix='Переадресация на неверный адрес')
