# about/urls.py
from django.urls import path
from . import views


app_name = 'about'

urlpatterns = [
    path('author/', views.AboutAuthorView.as_view(), name='author'),
    path('tech/', views.AboutTechView.as_view(), name='tech'),
    path('contact/', views.AboutContactView.as_view(), name='contact'),
]