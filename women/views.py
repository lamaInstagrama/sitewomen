from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView

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


class ShowPost(DetailView):
    model = Women
    template_name = 'women/women_info.html'
    slug_url_kwarg = 'slug_name'
    # pk_url_kwarg = ''  # Для первичных ключей
    context_object_name = 'woman'

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs.get(self.slug_url_kwarg))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = context.get(self.context_object_name).tags.all()
        return context


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


class AddPage(CreateView):
    form_class = AddPostForm
    # model = Women
    # fields = '__all__'
    template_name = 'women/add_page.html'
    success_url = reverse_lazy('women_start_page')

    extra_context = {
        'menu': menu,
        'title': 'Добавить статью'
    }


class UpdatePage(UpdateView):
    form_class = AddPostForm
    model = Women
    # fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'women/add_page.html'
    success_url = reverse_lazy('women_start_page')
    extra_context = {
        'menu': menu,
        'title': 'Добавить статью'
    }
    slug_url_kwarg = 'slug_name'


class DeletePost(DeleteView):
    # form_class = AddPostForm
    model = Women  # Change 3
    template_name = 'women/add_page.html'
    success_url = reverse_lazy('women_start_page')
    extra_context = {
        'menu': menu,
        'title': 'Добавить статью'
    }
    slug_url_kwarg = 'slug_name'



def contact(request: HttpRequest):
    return render(request, 'women/contact.html', context={'data': DataTemplate('Ilya', 'Buyanov') })
    # return HttpResponse('Обратная связь')


def login(request: HttpRequest):
    return HttpResponse('Авторизация')
