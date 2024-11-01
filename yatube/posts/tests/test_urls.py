# posts/tests/test_urls.py
from django.contrib.auth.models import User
from django.test import TestCase, Client # type: ignore
from django.urls import reverse
from http import HTTPStatus



class StaticURLTests(TestCase):
    def setUp(self):
        # Устанавливаем данные для тестирования
        # Создаём экземпляр клиента. Он неавторизован.
        self.guest_client = Client()
        # Создаём экземпляр клиента. Он авторизован.
        self.authorized_client = Client()
        
        # Создаём тестового пользоватееля в БД        
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Логинимся тестовым пользователем
        self.authorized_client.login(username='testuser', password='testpassword')
        
       
        self.urls = {
            'index' : 'posts:index',
            'group_list' : 'posts:group_list',
        }
        

    def test_homepage(self):
        """При переходе на страницу, она доступна по ожидаемому адресу. Cтатус 200"""
        url = reverse(self.urls['index'])
        # Создаем экземпляр клиента
        # Делаем запрос к главной странице и проверяем статус
        response = self.guest_client.get(url)
        # Утверждаем, что для прохождения теста код должен быть равен 200
        self.assertEqual(response.status_code, HTTPStatus.OK)
        
        
    def test_group_list_page(self):
        """При переходе на страницу, она доступна по ожидаемому адресу. Cтатус 200 """
        url = reverse(self.urls['group_list'])
        # Создаем экземпляр клиента
        # Делаем запрос к главной странице и проверяем статус
        response = self.authorized_client.get(url)
        # Утверждаем, что для прохождения теста код должен быть равен 200
        self.assertEqual(response.status_code, HTTPStatus.OK)
        
