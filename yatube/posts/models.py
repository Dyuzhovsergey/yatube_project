from typing import Any
from django.db import models

from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Group(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Название группы')
    slug = models.SlugField(
        unique=True,
        verbose_name='Уникальный адрес группы')
    description = models.TextField(verbose_name='Описание сообщества')
    
    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title
    
    
class Post(models.Model):
    text = models.TextField(verbose_name="Полный текст поста",
                            help_text='Введите текст поста')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации",
                                    help_text='Дата, в которую опубликован пост')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name = "Автор",
        help_text='Выберете автора поста'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Группа",
        help_text='Группа, к которой будет относиться пост')

    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )
    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        
    def __str__(self):
        return self.text[:15] 
    
    
class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Пост",
        help_text="Пост, к которому относится комментарий"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Автор",
        help_text="Автор комментария"
    )
    text = models.TextField(
        verbose_name="Текст комментария",
        help_text="Введите текст комментария"
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации",
        help_text="Дата и время публикации комментария"
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'
        
    def __str__(self):
        return self.text[:15] 
    

    
class Follow(models.Model):
    # объект пользователя, который подписывается
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name="Подписчик",
        help_text="Подписчик на автора"
    )
    # объект пользователя, на которого подписываются
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name = "Автор",
        help_text='Автора поста'
    )

    # class Meta:
    #     ordering = ('-created',)
    #     verbose_name = 'Подписка'
    #     verbose_name_plural = 'Подписки'
        
    # def __str__(self):
    #     return self.text[:15] 
