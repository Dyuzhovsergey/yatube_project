# deals/tests/tests_models.py
from django.test import TestCase

from posts.models import Post, Group

from django.contrib.auth import get_user_model

User = get_user_model()

class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(username='auth', password='password')
        
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def test_models_have_correct_object_name(self):
        """В поле __str__  объекта post и group записано значение поля post.text и group.title"""
        post = PostModelTest.post
        expected_object_text = post.text
        
        group = PostModelTest.group
        expected_object_title = group.title
        
        self.assertEqual(expected_object_text, str(post))
        self.assertEqual(expected_object_title, str(group))
        

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        post = PostModelTest.post
        field_verboses = {
            'text': 'Полный текст поста',
            'pub_date': 'Дата публикации',
            'group': 'Группа',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value)

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        post = PostModelTest.post
        field_help_texts = {
            'text': 'Введите текст поста',
            'pub_date': 'Дата, в которую опубликован поост',
            'group': 'Группа, к которой будет относиться пост',
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value) 