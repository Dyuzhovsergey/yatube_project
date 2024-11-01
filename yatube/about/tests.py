from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from http import HTTPStatus

# Create your tests here.
class StaticURLTests(TestCase):
    def setUp(self):
        # Устанавливаем данные для тестирования
        # Создаём экземпляр неавтклиента. Он неавторизован.
        self.guest_client = Client()
       
        self.urls = {
            'author' : 'about:author',
            'tech' : 'about:tech',
            'contact' : 'about:contact',
        }
        
    def test_author_page(self):
        """При переходе на страницу, она доступна по ожидаемому адресу. Cтатус 200 """
        url = reverse(self.urls['author'])
        # Создаем экземпляр клиента
        # Делаем запрос к странице с технологиями и проверяем статус
        response = self.guest_client.get(url)
        # Утверждаем, что для прохождения теста код должен быть равен 200
        self.assertEqual(response.status_code, HTTPStatus.OK)   

    def test_tech_page(self):
        """При переходе на страницу, она доступна по ожидаемому адресу. Cтатус 200 """
        url = reverse(self.urls['tech'])
        # Создаем экземпляр клиента
        # Делаем запрос к странице с технологиями и проверяем статус
        response = self.guest_client.get(url)
        # Утверждаем, что для прохождения теста код должен быть равен 200
        self.assertEqual(response.status_code, HTTPStatus.OK)   


    def test_contact_page(self):
        """При переходе на страницу, она доступна по ожидаемому адресу. Cтатус 200 """
        url = reverse(self.urls['contact'])
        # Создаем экземпляр клиента
        # Делаем запрос к странице с технологиями и проверяем статус
        response = self.guest_client.get(url)
        # Утверждаем, что для прохождения теста код должен быть равен 200
        self.assertEqual(response.status_code, HTTPStatus.OK)                   