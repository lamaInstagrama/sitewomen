from django.contrib import admin, messages
from django.db.models import F
from django.db.models.functions import Length
from django.utils.safestring import mark_safe

from women.models import Women, Category


class MarriedFilter(admin.SimpleListFilter):
    title = 'Статус женщин'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('married', 'Замужем'),
            ('single', 'Не замужем')
        ]

    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(husband__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(husband__isnull=True)


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'photo', 'post_photo', 'content', 'cat', 'tags']
    readonly_fields = ['post_photo']
    filter_horizontal = ['tags']
    prepopulated_fields = {'slug': ('title',)}
    # readonly_fields = ['slug']
    # exclude = ['tags', 'is_published']
    list_display = ['pk', 'title', 'slug', 'post_photo', 'time_update', 'is_published', 'cat', 'count_len']
    list_display_links = ['pk', 'title']
    ordering = ['time_update', 'title']
    list_editable = ['is_published']
    list_per_page = 5
    actions = ['set_published', 'set_unpublished']
    search_fields = ['title', 'cat__name']
    list_filter = [MarriedFilter, 'cat__name', 'is_published']
    save_on_top = True

    @staticmethod
    @admin.display(description='Фото')
    def post_photo(women: Women):
        if women.photo:
            return mark_safe(f"<img src='{women.photo.url}' width=50>")
        return 'No Photo'

    @staticmethod
    @admin.display(description='Количество символов', ordering=Length(F('content')))
    def count_len(women: Women):
        return f'Длина статьи {len(women.content)} символов'

    @admin.display(description='Опубликовать выбранные статьи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f'Опубликовано {count} статей')

    @admin.display(description='Снять с публикации выбранные статьи')
    def set_unpublished(self, request, queryset):
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f'Снято с публикации {count} статей', level=messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']



