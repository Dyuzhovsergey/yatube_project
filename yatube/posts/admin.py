from django.contrib import admin

# Register your models here.
from .models import Group, Post


class PostAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group',
    )
    
    list_editable = ('group',) 
    
    # Добавляем интерфейс для поиска по тексту постов
    search_fields = ('text',) 
    # Добавляем возможность фильтрации по дате
    list_filter = ('pub_date',)
    
    empty_value_display = '-пусто-'  

# При регистрации модели Post источником конфигурации для неё назначаем
# класс PostAdmin

admin.site.register(Post, PostAdmin)
admin.site.register(Group)  
