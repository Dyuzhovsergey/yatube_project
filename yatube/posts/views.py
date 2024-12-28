from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group, Comment, Follow

from django.views.generic.edit import CreateView
from .forms import PostForm, CommentForm

from django.views.decorators.cache import cache_page

from django.contrib.auth import get_user_model

from django.contrib.auth.decorators import login_required

User = get_user_model()

# кэш на 15 минут
# @cache_page(60 * 15)
def index(request):
    template = 'posts/index.html'
    title_index = "Главная страница"
    post_list = Post.objects.order_by('-pub_date')[:20]
    
    posts_all_count = Post.objects.count()
    
    # Показывать по 10 записей на странице.
    paginator = Paginator(post_list, 10) 
    
    # Из URL извлекаем номер запрошенной страницы - это значение параметра page
    page_number = request.GET.get('page')
    
    # Получаем набор записей для страницы с запрошенным номером
    page_obj = paginator.get_page(page_number)
    
    context = {
        'posts_all_count' : posts_all_count,
        'page_obj': page_obj,
        'title_index' : title_index,    
        'index': True,    
    }
    return render(request, template, context)  


def group_list(request):
    template = 'posts/group_list.html'
    title = "Список групп"
    groups = Group.objects.all()
    context = {
        'title': title,
        'groups' : groups
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_posts.html'
    title = "Список постов в группе"
    group = get_object_or_404(Group, slug=slug)    
 
    # Метод .filter позволяет ограничить поиск по критериям.
    # Это аналог добавления
    # условия WHERE group_id = {group_id}
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,  
        'title': title,
        'group': group,
    }
    return render(request, template, context)


def profile(request, username):
    # Здесь код запроса к модели и создание словаря контекста
    template = 'posts/profile.html'
    title = "Профайл пользователя" 

    author_posts = get_object_or_404(User, username=username) 
    # Подписан ли пользователь request.user на автора постов в профайле author_posts
    following = Follow.objects.filter(user=request.user, author=author_posts).exists()

    posts_count = Post.objects.filter(author=author_posts).count()
        
    post_list = Post.objects.filter(author=author_posts).order_by('-pub_date')
    
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    
    # Получаем набор записей для страницы с запрошенным номером
    page_obj = paginator.get_page(page_number)
   
    context = {
        'title': title,
        'page_obj' : page_obj,
        'posts_count' : posts_count,
        'author_posts' : author_posts,
        'following' : following,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, id = post_id)
    title = post.text[:30]
    number = Post.objects.filter(author=post.author).count()
    
    form = CommentForm()
    comments = Comment.objects.filter(post=post_id)

    context = {
        'number':number,
        'title': title,
        'post' : post,
        'form' : form,
        'comments' : comments,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/post_create.html'
    
    if request.method == 'POST':
        form = PostForm(request.POST, files=request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', username=request.user.username)
        else:
            return render(request, template, {'form': form})
    else:
        form = PostForm()
        return render(request, template, {'form': form})


@login_required
def post_edit(request, post_id):
    template = 'posts/post_create.html'
        
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post.id)
   
    if request.method == 'POST':
        form = PostForm(request.POST , files=request.FILES or None, instance=post)

        if form.is_valid():
            form.save()
            return redirect('posts:post_detail', post_id=post.id)
        else:
            return render(request, template, {'form': form})
    else:
        
        form = PostForm(instance=post)
        context = {
        'post':post,
        'form':form,
        'is_edit': True,
    }
        return render(request, template, context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id) 


@login_required
def follow_index(request):
    template = 'posts/follow.html'
    title_follow = "Страница постов авторов, на которых вы подписаны"
    
    # Получаем список авторов, на которых подписан текущий пользователь
    authors = Follow.objects.filter(user=request.user).values_list('author', flat=True)
    
    # Получаем посты только от этих авторов
    posts = Post.objects.filter(author__in=authors).order_by('-pub_date')
    
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'title_follow': title_follow,
        'page_obj': page_obj,
        'follow': True, 
    }
    return render(request, template, context)



@login_required
def profile_follow(request, username):
    # Подписаться на автора
    author = get_object_or_404(User, username=username)

    # Проверяем, существует ли подписка, если нет - создаем
    Follow.objects.get_or_create(user=request.user, author=author)
    
    return redirect('posts:profile', username=username)



@login_required
def profile_unfollow(request, username):
    # Отписаться на автора
    author = get_object_or_404(User, username=username)

    Follow.objects.filter(user=request.user, author=author).delete()
    
    return redirect('posts:profile', username=username)


