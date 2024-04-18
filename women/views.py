from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView

from women.models import Women, Category, TagPost, UploadFiles
from women.forms import AddPostForm, UploadFileFrom
from women.utils import DataMixin


class DataTemplate:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def get_info(self):
        return self.first_name + " " + self.last_name


class WomenHome(DataMixin, ListView):
    template_name = 'women/main_title.html'
    context_object_name = 'data_db'
    title_page = 'Главная страница'

    def get_queryset(self):
        return Women.published.all()


class Button(TemplateView):
    template_name = 'women/button.html'


class WomenCategory(DataMixin, ListView):
    template_name = 'women/main_title.html'
    context_object_name = 'data_db'

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        category = get_object_or_404(Category, slug=self.kwargs.get('cat_slug'))
        context['category'] = category
        context['title'] = f'Рубрика: {category.name}'
        return context


class TagPostList(DataMixin, ListView):
    template_name = 'women/main_title.html'
    context_object_name = 'data_db'

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
    return render(request, 'women/about.html', context={'title': 'О сайте', 'form': form})


class AddPage(DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/add_page.html'
    success_url = reverse_lazy('women_start_page')
    title = 'Добавить статью'


class UpdatePage(DataMixin, UpdateView):
    form_class = AddPostForm
    model = Women
    template_name = 'women/add_page.html'
    success_url = reverse_lazy('women_start_page')
    title = 'Редактировать статью'
    slug_url_kwarg = 'slug_name'


class DeletePost(DataMixin, DeleteView):
    model = Women
    template_name = 'women/add_page.html'
    success_url = reverse_lazy('women_start_page')
    title = 'Удалить статью'
    slug_url_kwarg = 'slug_name'


def contact(request: HttpRequest):
    return render(request, 'women/contact.html', context={'data': DataTemplate('Ilya', 'Buyanov') })
    # return HttpResponse('Обратная связь')


def login(request: HttpRequest):
    return HttpResponse('Авторизация')
