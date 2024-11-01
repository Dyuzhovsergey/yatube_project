# users/tests/test_urls.py
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
        
        self.uid = 'some-uid64-value'
        self.token = 'some-token-value'
    
    def test_signup_page(self):
        """При переходе на страницу signup, она доступна по ожидаемому адресу. Cтатус 200"""
        url = reverse('users:signup')
        # Создаем экземпляр клиента
        # Делаем запрос к главной странице и проверяем статус
        response = self.guest_client.get(url)
        # Утверждаем, что для прохождения теста код должен быть равен 200
        self.assertEqual(response.status_code, HTTPStatus.OK)
                
    def test_urls_authorized_users(self):
        """URL-адрес использует соответствующий шаблон у НЕ авторизованного пользователя."""
        # Шаблоны по адресам
        urls = {
            'users:logout': HTTPStatus.OK,
            'users:password_change_form' : HTTPStatus.OK,
            'users:password_change_done' : HTTPStatus.OK,
            'users:password_reset_form' : HTTPStatus.OK,
            'users:password_reset_done' : HTTPStatus.OK,
            'users:password_reset_complete' : HTTPStatus.OK,
        }
        for address, expected_status in urls.items():
            with self.subTest(address=address):
                response = self.guest_client.get(reverse(address))
                self.assertEqual(response.status_code, expected_status)

    def test_password_reset_confirm_url(self):
        """Тестирование URL для входа по ссылке для восстановления пароля"""
        # Используем `reverse` для построения URL с аргументами
        url = reverse('users:password_reset_confirm', kwargs={'uidb64': self.uid, 'token': self.token})

        # Выполняем GET-запрос к URL
        response = self.client.get(url)

        # Проверяем, что статус-код соответствует ожидаемому
        self.assertEqual(response.status_code, HTTPStatus.OK)