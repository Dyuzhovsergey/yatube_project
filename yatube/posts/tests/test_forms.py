# posts/tests/tests_form.py
import shutil
import tempfile

from posts.forms import PostForm
from django.contrib.auth.models import User
from posts.models import Post, Group
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

# Создаем временную папку для медиа-файлов;
# на момент теста медиа папка будет переопределена
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


# Для сохранения media-файлов в тестах будет использоваться
# временная папка TEMP_MEDIA_ROOT, а потом мы ее удалим

@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)

class PostImageTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем пользователя
        cls.user = User.objects.create_user(username='testuser', password='12345')
        
        # Создаем тестовую группу
        cls.group = Group.objects.create(
            title='Test Group',
            slug='test-group',
            description='A test group'
            )
        # Создаем байт-последовательность
        cls.small_gif = (            
             b'\x47\x49\x46\x38\x39\x61\x02\x00'
             b'\x01\x00\x80\x00\x00\x00\x00\x00'
             b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
             b'\x00\x00\x00\x2C\x00\x00\x00\x00'
             b'\x02\x00\x01\x00\x00\x02\x02\x0C'
             b'\x0A\x00\x3B'
        )
        
        # Создаем тестовое изображение
        cls.image = SimpleUploadedFile(
            name='test_image.jpg',
            content=cls.small_gif,
            content_type='image/jpeg'
        )
        
        # Создаем тестовый пост
        cls.post = Post.objects.create(
            text='This is a test post',
            author=cls.user,
            group=cls.group,
            image=cls.image
        )

    def setUp(self):
        
        # Создаем клиент для тестирования
        self.client = Client()
        self.authorized_client = Client()
        # Авторизуем клиент для тестирования
        self.authorized_user = User.objects.create_user(username='authorized_user', password='12345')
        self.authorized_client.force_login(self.authorized_user)
 
    def tearDown(self):
        # Удаляем временную директорию после завершения тестов
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_image_in_context_index_page(self):
        response = self.client.get(reverse('posts:index'))  
        self.assertEqual(response.status_code, 200)
        self.assertIn('page_obj', response.context)

        first_post = response.context['page_obj'][0]
        self.assertEqual(first_post.image, PostImageTest.post.image)
        
    def test_image_in_context_profile_page(self):
        response = self.client.get(reverse('posts:profile', kwargs={'username': PostImageTest.user.username}))  
        self.assertEqual(response.status_code, 200)
        self.assertIn('page_obj', response.context)

        first_post = response.context['page_obj'][0]
        self.assertEqual(first_post.image, PostImageTest.post.image)

    def test_image_in_context_group_page(self):
        response = self.client.get(reverse('posts:group', kwargs={'slug': PostImageTest.group.slug})) 
        self.assertEqual(response.status_code, 200)
        self.assertIn('page_obj', response.context)

        first_post = response.context['page_obj'][0]
        self.assertEqual(first_post.image, PostImageTest.post.image)      
        
    def test_image_in_context_post_detail_page(self):
        response = self.client.get(reverse('posts:post_detail', kwargs={'post_id': PostImageTest.post.id})) 
        self.assertEqual(response.status_code, 200)
        self.assertIn('post', response.context)
        
        post_from_context = response.context['post']
        self.assertEqual(post_from_context.image, PostImageTest.post.image)        
        
    def test_create_task(self):
            """Валидная форма создает запись в Post."""
            # Подсчитаем количество записей в Task
            posts_count = Post.objects.count()  
            # Для тестирования загрузки изображений 
            # берём байт-последовательность картинки, 
            # состоящей из двух пикселей: белого и чёрного
            
            uploaded = SimpleUploadedFile(
            name='test_form_image.jpg',
            content=PostImageTest.small_gif,  # Используем small_gif из PostImageTest
            content_type='image/jpeg'
            )

            form_data = {
                'text': 'Тестовый текст',
                'group': PostImageTest.group.id, 
                'image': uploaded,
            }
                
            # Отправляем POST-запрос
            response = self.authorized_client.post(
                reverse('posts:post_create'),
                data=form_data,
                follow=True
            )

            # Проверяем, сработал ли редирект
            self.assertRedirects(response, reverse('posts:profile', kwargs={'username': self.authorized_user.username}))
            
            # Проверяем, увеличилось ли число постов
            self.assertEqual(Post.objects.count(), posts_count + 1)
             
            # Проверяем, проверяем появилось ли изображение в посте после POST
            self.assertTrue(Post.objects.filter(image='posts/test_form_image.jpg').exists()) 











