from django.urls import path, re_path
from women import views

urlpatterns = [
    path('', views.main_page, name='women_start_page'),
    re_path(r'button(?P<num>\d*)/', views.button),
    path('about/', views.about, name='about'),
    path('add_page/', views.add_page, name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path(r'<slug:slug_name>/', views.info_women, name='post'),
    path(r'category/<slug:cat_slug>/', views.show_category, name='category'),
    path('tag/<slug:tag_slug>/', views.show_tag_postlist, name='tag'),
    # path(r'<slug:slug_name>/', views.info_women_redirect, name='women_post_redirect'),
]