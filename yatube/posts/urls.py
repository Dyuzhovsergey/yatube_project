# posts/urls.py
from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('group_list/', views.group_list, name = 'group_list'),
    path('group/<slug:slug>/', views.group_posts, name= 'group'),
    # Профайл пользователя
    path('profile/<str:username>/', views.profile, name='profile'),
    # Просмотр записи
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    # Создание записи
    path('create/', views.post_create, name='post_create'),
    # Изменеие записи
    path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit'),
]





