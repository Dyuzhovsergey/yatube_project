# posts/tests/test_urls.py
from django.contrib.auth.models import User
from django.test import TestCase, Client # type: ignore


class StaticURLTests(TestCase):
    def setUp(self):
        # Устанавливаем данные для тестирования
        # Создаём экземпляр клиента. Он неавторизован.
        self.guest_client = Client()
        # Создаём экземпляр клиента. Он авторизован.
        self.test_client = Client()
        
        # Создаём тестового пользоватееля в БД        
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Логинимся тестовым пользователем
        self.test_client.login(username='testuser', password='testpassword')
        

    def test_homepage(self):
        # Создаем экземпляр клиента
        # Делаем запрос к главной странице и проверяем статус
        response = self.guest_client.get('/')
        # Утверждаем, что для прохождения теста код должен быть равен 200
        self.assertEqual(response.status_code, 200)
        
    def test_group_list_page(self):
        # Создаем экземпляр клиента
        # Делаем запрос к главной странице и проверяем статус
        response = self.test_client.get('/group_list/')
        # Утверждаем, что для прохождения теста код должен быть равен 200
        self.assertEqual(response.status_code, 200)
        
    def test_techpage(self):
        # Создаем экземпляр клиента
        # Делаем запрос к странице с технологиями и проверяем статус
        response = self.guest_client.get('/about/tech/')
        # Утверждаем, что для прохождения теста код должен быть равен 200
        self.assertEqual(response.status_code, 200)    