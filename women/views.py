from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.views import View
from django.views.generic import TemplateView, ListView

from women.models import Women, Category, TagPost, UploadFiles
from women.forms import AddPostForm, UploadFileFrom
import uuid

menu = [
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить статью", 'url_name': 'add_page'},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "Войти", 'url_name': 'login'}
        ]


class DataTemplate:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def get_info(self):
        return self.first_name + " " + self.last_name


# Create your views here.
# def main_page(request: HttpRequest):
#     data_db = Women.published.all()
#     categories = Category.objects.all()
#     tags = TagPost.objects.all()
#
#     data = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'data_db': data_db,
#         'categories': categories,
#         'tags': tags,
#
#     }
#     return render(request, 'women/main_title.html', context=data)


class WomenHome(ListView):
    template_name = 'women/main_title.html'
    context_object_name = 'data_db'
    extra_context = {
        'title': 'Главная страница',
        'menu': menu,
        'categories': Category.objects.all(),
        'tags': TagPost.objects.all(),
    }

    def get_queryset(self):
        return Women.published.all()


class Button(TemplateView):
    template_name = 'women/button.html'


def show_category(request: HttpRequest, cat_slug: str):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Women.published.filter(cat_id=category.pk)
    categories = Category.objects.all()
    tags = TagPost.objects.all()

    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'data_db': posts,
        'categories': categories,
        'tags': tags,
    }

    return render(request, 'women/main_title.html', context=data)


class WomenCategory(ListView):
    template_name = 'women/main_title.html'
    context_object_name = 'data_db'

    extra_context = {
        'menu': menu,
        'categories': Category.objects.all(),
        'tags': TagPost.objects.all(),
    }

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        category = get_object_or_404(Category, slug=self.kwargs.get('cat_slug'))
        context['category'] = category
        context['title'] = f'Рубрика: {category.name}'
        return context


class TagPostList(ListView):
    template_name = 'women/main_title.html'
    context_object_name = 'data_db'
    extra_context = {
        'menu': menu,
        'categories': Category.objects.all(),
        'tags': TagPost.objects.all(),
    }

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs.get('tag_slug'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(TagPost, slug=self.kwargs.get('tag_slug'))
        context['title'] = f'Тег: {tag.tag}'
        return context


def info_women(request: HttpRequest, slug_name):
    if not slug_name:
        return redirect('women_post_redirect')
    woman = get_object_or_404(Women, slug=slug_name)
    tags = woman.tags.all()
    context = {
        'woman': woman,
        'tags': tags,
    }

    return render(request, 'women/women_info.html', context=context)


def info_women_redirect(request: HttpRequest):
    return HttpResponse('Какая то ошибка :(')


def about(request: HttpRequest):
    if request.POST:
        form = UploadFileFrom(request.POST, request.FILES)
        if form.is_valid():
            # handle_uploaded_file(form.cleaned_data['file'])  # handle_uploaded_file(form.cleaned_data['file'])
            UploadFiles.objects.create(file=form.cleaned_data.get('file'))
    else:
        form = UploadFileFrom()
    return render(request, 'women/about.html', context={'menu': menu, 'title': 'О сайте', 'form': form})


def add_page(request: HttpRequest):
    if request.POST:
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('women_start_page')
    else:
        form = AddPostForm()
    return render(request, 'women/add_page.html', context={'menu': menu, 'title': 'Добавить статью', 'form': form})


class AddPage(View):
    def get(self, request):
        form = AddPostForm()
        return render(request, 'women/add_page.html', context={'menu': menu, 'title': 'Добавить статью', 'form': form})

    def post(self, request):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('women_start_page')

        return render(request, 'women/add_page.html', context={'menu': menu, 'title': 'Добавить статью', 'form': form})

def contact(request: HttpRequest):
    return render(request, 'women/contact.html', context={'data': DataTemplate('Ilya', 'Buyanov') })
    # return HttpResponse('Обратная связь')


def login(request: HttpRequest):
    return HttpResponse('Авторизация')
