from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from posts.models import Post, Group

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth', password='password')
        cls.user_author = User.objects.create_user(username='author', password='password')
        # Создадим запись в БД для проверки доступности адреса task/test-slug/
        
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            group=cls.group,
        )

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем пользователя
        # Создаем второй клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(PostURLTests.user)
        

    def test_urls_guest_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон у НЕ авторизованного пользователя.."""
        # Шаблоны по адресам
        templates_url_names = {
            '/': 'posts/index.html',
            '/group_list/': 'posts/group_list.html',
            '/group/test-slug/': 'posts/group_posts.html',
            '/profile/auth/': 'posts/profile.html',
            '/posts/1/': 'posts/post_detail.html',
            '/unexisting_page/': 'core/404.html',
        }
        for address, template  in templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)   
                
                
                
    def test_urls_authorized_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон у авторизованного пользователя."""
        # Шаблоны по адресам
        templates_url_names = {
            '/create/': 'posts/post_create.html',
            '/posts/1/edit/': 'posts/post_create.html',
        }
        for address, template  in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)             
    
