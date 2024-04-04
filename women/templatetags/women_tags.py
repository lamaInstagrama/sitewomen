import women.views as views
from django import template


register = template.Library()
"""
Создаю экземпляр этого класса, через него происходит регистрация собственных шаблонных тэгов
"""


@register.simple_tag(name='get_menu')
def get_categories():
    return views.menu


@register.inclusion_tag('women/show_menu.html')
def show_menu():
    menu = views.menu
    return {'menu': menu}
