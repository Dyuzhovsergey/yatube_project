# users/urls.py
from django.urls import path
from . import views

from django.contrib.auth.views import LogoutView , LoginView

app_name = 'users'

urlpatterns = [
        # Регистрация
    path('signup/', views.SignUp.as_view(), name='signup'),
        # Выход
    path('logout/', LogoutView.as_view(template_name='users/logged_out.html'), name = 'logout'),
        # Авторизация / Вход
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
        
        # Смена пароля
    path('password_change/', LoginView.as_view(template_name='users/password_change_form.html'), name='password_change_form'),
        # Сообщение об успешном изменении пароля
    path('password_change/done/', LoginView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),
        
        # Восстановление пароля
    path('password_reset/', LoginView.as_view(template_name='users/password_reset_form.html'), name='password_reset_form'),
        # Сообщение об отправке ссылки для восстановления пароля
    path('password_reset/done/', LoginView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
        
        # Вход по ссылке для восстановления пароля
    path('reset/<uidb64>/<token>/', LoginView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'), 
        # Сообщение об успешном восстановлении пароля 
    path('reset/done/', LoginView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]          