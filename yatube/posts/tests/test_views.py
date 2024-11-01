# posts/tests/test_views.py
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms 

from posts.models import Post, Group
from django.core.paginator import Page

from posts.forms import PostForm

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создадим запись в БД
        cls.user = User.objects.create_user(username='TestUser', password='password')
       
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        
        cls.group_other = Group.objects.create(
            title='Тестовая группа другая',
            slug='test-slug-other',
            description='Тестовое описание другое',
        )
        
        #   Создаем 1 пост
        # cls.post = Post.objects.create(
        #     text='Тестовый текст',
        #     author=cls.user,
        #     group=cls.group,
        # )
        
        #   Создаем 20 постов
        cls.posts = [Post.objects.create(
            text=f'Test Post {i}',
            author=cls.user,
            group=cls.group
        ) for i in range(20)]

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PostPagesTests.user)

    # Проверяем используемые шаблоны
    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Собираем в словарь пары "имя_html_шаблона: reverse(name)"
        templates_pages_names = {
            reverse('posts:index') : 'posts/index.html',
            reverse('posts:group_list'):'posts/group_list.html',
            reverse('posts:group', kwargs={'slug': 'test-slug'}): 'posts/group_posts.html' ,
            reverse('posts:profile', kwargs={'username': 'TestUser'}): 'posts/profile.html' ,
            reverse('posts:post_detail', kwargs={'post_id': 1}):'posts/post_detail.html',
            reverse('posts:post_create'):'posts/post_create.html',
            reverse('posts:post_edit',  kwargs={'post_id': 1}):'posts/post_create.html',
        }
        # Проверяем, что при обращении к name вызывается соответствующий HTML-шаблон
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)


    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.client.get(reverse('posts:index'))
        # Словарь ожидаемых типов объектов в контексте
        context_fields_type = {
            'title_index': str,
            'posts_all_count': int,
            'page_obj': Page,
        }

        # Проверяем, что объекты в словаре context соответствуют ожиданиям
        for value, expected in context_fields_type.items():
            with self.subTest(value=value):
                context_value = response.context.get(value)
                # Проверяет, что объект контекста является экземпляром
                # указанного класса
                self.assertIsInstance(context_value, expected)

        # Дополнительно проверяем значение title_index

    def test_detail_pages_index_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.client.get(reverse('posts:index'))
        context_fields = {
            'title_index': "Главная страница",
            'posts_all_count': Post.objects.count(),
        }
        # Проверяем, что объекты в словаре context соответствуют ожиданиям
        for value, expected in context_fields.items():
            with self.subTest(value=value):
                context_value = response.context.get(value)
                self.assertEqual(context_value, expected)
                
        # Проверяем, что на странице отображается 10 постов
        self.assertEqual(len(response.context['page_obj']), 10)    
        response = self.client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 10)                 

    def test_detail_pages_group_posts_show_correct_context(self):
        """Шаблон group_posts сформирован с правильным контекстом."""
        response = self.client.get(reverse('posts:group', kwargs={'slug': 'test-slug'}))
        context_fields = {
            'title': "Список постов в группе",
            'group' : PostPagesTests.group,
        }
        # Проверяем, что объекты в словаре context соответствуют ожиданиям
        for value, expected in context_fields.items():
            with self.subTest(value=value):
                context_value = response.context.get(value)
                self.assertEqual(context_value, expected)

        # Извлечение постов из page_obj
        context_posts = list(response.context['page_obj'].object_list)
        # Ожидаемые посты из базы данных (учитываем сортировку и ограничение по количеству)
        expected_posts = list(Post.objects.filter(group=PostPagesTests.group).order_by('-pub_date')[:5])
        # Сравнение списков объектов
        self.assertEqual(context_posts, expected_posts)
        
        # Проверяем, пажинатор страницы group_posts
        self.assertEqual(len(response.context['page_obj']), 5)
        
        response = self.client.get(reverse('posts:group', kwargs={'slug': 'test-slug'}) + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 5)     


    def test_detail_pages_profile_show_correct_context(self):
        """Шаблон group_posts сформирован с правильным контекстом."""
        response = self.client.get(reverse('posts:profile', kwargs={'username': 'TestUser'}))
        context_fields = {
            'title': "Профайл пользователя",
            'user' : PostPagesTests.user,
        }
        # Проверяем, что объекты в словаре context соответствуют ожиданиям
        for value, expected in context_fields.items():
            with self.subTest(value=value):
                context_value = response.context.get(value)
                self.assertEqual(context_value, expected)

        context_posts = list(response.context['page_obj'].object_list)
        # Ожидаемые посты из базы данных (учитываем сортировку и ограничение по количеству)

        expected_posts = list(Post.objects.filter(author=PostPagesTests.user).order_by('-pub_date')[:len(context_posts)])
        # Сравнение списков объектов
        self.assertEqual(context_posts, expected_posts)
        
        # Проверяем, пажинатор страницы profile 
        self.assertEqual(len(response.context['page_obj']), 10)  
        
        
    def test_detail_pages_post_detail_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.client.get(reverse('posts:post_detail', kwargs={'post_id': 1}))

        context_posts = response.context['post']
        # Ожидаемые посты из базы данных (учитываем сортировку и ограничение по количеству)

        expected_posts = Post.objects.get(id=1)
        # Сравнение списков объектов
        self.assertEqual(context_posts, expected_posts)
        
    def test_detail_pages_create_post_show_correct_context(self):
        """Шаблон create_post сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        
        self.assertIn('form', response.context)
        # Извлечение формы из контекста
        form = response.context['form']
        self.assertIsInstance(form, PostForm)
        
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for field, field_type in form_fields.items():
            with self.subTest(field=field):
                form_field = response.context.get('form').fields.get(field)
                # Проверяет, что поле формы является экземпляром
                # указанного класса
                self.assertIsInstance(form_field, field_type)
 
    def test_detail_pages_post_edit_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_edit', kwargs={'post_id': 1}))
        
        self.assertIn('form', response.context)
        # Извлечение формы из контекста
        form = response.context['form']
        self.assertIsInstance(form, PostForm)
        
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
            'image': forms.fields.ImageField,
        }

        for field, field_type in form_fields.items():
            with self.subTest(field=field):
                form_field = response.context.get('form').fields.get(field)
                # Проверяет, что поле формы является экземпляром
                # указанного класса
                self.assertIsInstance(form_field, field_type)
                

    def test_post_appears_on_correct_pages(self):

         # Проверяем, что пост появился на главной странице
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertContains(response, 'Test Post')

        # Проверяем, что пост появился на странице выбранной группы
        response = self.authorized_client.get(reverse('posts:group',kwargs={'slug': PostPagesTests.group.slug}))
        self.assertContains(response, 'Test Post')

        # Проверяем, что пост появился в профайле пользователя
        response = self.authorized_client.get(reverse('posts:profile', kwargs={'username': PostPagesTests.user.username}))
        self.assertContains(response, 'Test Post')

        # Проверяем, что пост не появился в другой группе
        response = self.authorized_client.get(reverse('posts:group', kwargs={'slug': PostPagesTests.group_other.slug}))
        self.assertNotContains(response, 'Test Post')                
