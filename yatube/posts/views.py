from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group, Comment

from django.views.generic.edit import CreateView
from .forms import PostForm, CommentForm

from django.contrib.auth import get_user_model

from django.contrib.auth.decorators import login_required

User = get_user_model()

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
    user = get_object_or_404(User, username=username) 
    
    post_list = Post.objects.filter(author=user).order_by('-pub_date')
    
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    
    # Получаем набор записей для страницы с запрошенным номером
    page_obj = paginator.get_page(page_number)
   
    context = {
        'title': title,
        'user' : user,
        'page_obj' : page_obj,
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
    # Получите пост и сохраните его в переменную post.
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id) 
