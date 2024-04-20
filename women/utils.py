from women.models import Category, TagPost

menu = [
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить статью", 'url_name': 'add_page'},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "Войти", 'url_name': 'login'}
        ]


class DataMixin:
    extra_context = {}
    title_page = None
    categories = None
    tags = None
    paginate_by = 3

    def __init__(self):
        if 'menu' not in self.extra_context:
            self.extra_context['menu'] = menu

        if self.title_page:
            self.extra_context['title'] = self.title_page

        if self.categories is None:
            self.extra_context['categories'] = Category.objects.all()
        else:
            self.extra_context['categories'] = self.categories

        if self.tags is None:
            self.extra_context['tags'] = TagPost.objects.all()
        else:
            self.extra_context['tags'] = self.tags

