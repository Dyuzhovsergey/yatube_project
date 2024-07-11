from typing import Any
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Group(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название группы')
    slug = models.SlugField(unique=True, verbose_name='Уникальный адрес группы')
    description = models.TextField(verbose_name='Описание сообщества')

    def __str__(self):
        return self.title
    
class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)

    

    