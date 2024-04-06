from django import forms
from django.core.exceptions import ValidationError

from women.models import Category, Husband, Women


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категории', empty_label='Категория не выбрана')
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, label='Муж', empty_label='Не замужем')

    class Meta:
        model = Women
        fields = ('title', 'content', 'is_published', 'slug', 'cat', 'tags', 'husband')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5})
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
        if not (set(title) <= set(ALLOWED_CHARS)):
            raise ValidationError("Должны быть только русские символы, дефис и пробел.")
        return title


class UploadFileFrom(forms.Form):
    file = forms.ImageField(label='')


# Форма, не связанная с моделями
# class AddPostForm(forms.Form):
#     title = forms.CharField(max_length=255,
#                             min_length=5,
#                             error_messages={
#                                 'max_length': 'Имя актрисы не такое длинное',
#                                 'min_length': 'Имя актрисы не такое короткое',
#                                 'required': 'Нужно ввести имя!'
#                             },
#                             label='Заголовок',
#                             widget=forms.TextInput(
#                                 attrs={'class': 'form-input'}
#                             ))
#     slug = forms.SlugField(max_length=255,
#                            label='Слаг',
#                            validators=[
#                                MinLengthValidator(5, message='Минимум 5 символов'),
#                                MaxLengthValidator(100, message='Максимум 100 символов'),
#                            ])
#     content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label='Контент')
#     is_published = forms.BooleanField(required=False, label='Опубликовать', initial=True)
#     cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категории', empty_label='Категория не выбрана')
#     husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, label='Муж',
#                                      empty_label='Не замужем')
#     tags = forms.ModelMultipleChoiceField(queryset=TagPost.objects.all(),
#                                           label='Теги',
#                                           validators=(TagsValidator(),)
#                                           )
#
#     def clean_title(self):
#         title = self.cleaned_data.get('title')
#         ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
#         if not (set(title) <= set(ALLOWED_CHARS)):
#             raise ValidationError("Должны быть только русские символы, дефис и пробел.")
#         return title
