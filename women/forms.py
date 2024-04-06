from django import forms
from women.models import Category, Husband, TagPost


class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255,
                            min_length=5,
                            error_messages={
                                'max_length': 'Имя актрисы не такое длинное',
                                'min_length': 'Имя актрисы не такое короткое',
                                'required': 'Нужно ввести имя!'
                            },
                            label='Заголовок',
                            widget=forms.TextInput(
                                attrs={'class': 'form-input'}
                            ))
    slug = forms.SlugField(max_length=255, label='Слаг')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label='Контент')
    is_published = forms.BooleanField(required=False, label='Опубликовать', initial=True)
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категории', empty_label='Категория не выбрана')
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, label='Муж', empty_label='Не замужем')
    tags = forms.ModelMultipleChoiceField(queryset=TagPost.objects.all(), label='Теги')

