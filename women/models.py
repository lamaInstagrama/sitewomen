from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.shortcuts import reverse
from django.template.defaultfilters import slugify


class TagsValidator:
    code = 'tags'

    def __init__(self, message: str | None = None):
        self.message = message or 'Нельзя выбирать \'Блондинки\' и \'Брюнетки\' одновременно'

    def __call__(self, value, *args, **kwargs):
        objs = TagPost.objects.filter(tag__in=('Блондинки', 'Брюнетки')).values('pk')
        pks = set(str(tuple(obj.values())[0]) for obj in objs)
        if pks <= set(value):
            raise ValidationError(self.message, code=self.code, params={'value': value})


class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


class Women(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Не опубликовано'
        PUBLISHED = 1, 'Опубликовано'

    objects = models.Manager()
    published = PublishedModel()

    title = models.CharField(max_length=255, verbose_name='Имя женщины')
    content = models.TextField(blank=True, verbose_name='Биография')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices))
                                       , default=Status.DRAFT, verbose_name='Статус')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    photo = models.CharField(max_length=255, default='NoPhoto')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name='Категории')
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name='Тэги',
                                  validators=(TagsValidator(),))
    husband = models.OneToOneField('Husband', on_delete=models.SET_NULL, null=True, blank=True, related_name='married',
                                   verbose_name='Муж')

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post', args=(self.slug,))

    class Meta:
        verbose_name = 'Все мои женщины'
        verbose_name_plural = 'Все мои женщины'
        ordering = ['-time_create']

    def __str__(self):
        return self.title


class Husband(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField(null=True)
    m_count = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField(max_length=255, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', args=(self.slug,))


class TagPost(models.Model):
    tag = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', args=(self.slug,))
