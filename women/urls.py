from django.urls import path, re_path
from women import views

urlpatterns = [
    path('', views.WomenHome.as_view(), name='women_start_page'),
    re_path(r'button(?P<num>\d*)/', views.Button.as_view()),
    path('about/', views.about, name='about'),
    path('add_page/', views.AddPage.as_view(), name='add_page'),
    path('edit/<slug:slug_name>/', views.UpdatePage.as_view(), name='edit_page'),
    path('delete/<slug:slug_name>/', views.DeletePost.as_view(), name='delete_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path(r'<slug:slug_name>/', views.ShowPost.as_view(), name='post'),
    path(r'category/<slug:cat_slug>/', views.WomenCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name='tag'),
    # path(r'<slug:slug_name>/', views.info_women_redirect, name='women_post_redirect'),
]
