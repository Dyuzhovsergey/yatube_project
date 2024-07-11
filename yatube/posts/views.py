from django.shortcuts import HttpResponse
from django.shortcuts import render
from .models import Post



# def index(request):
#     template = 'posts/index.html'
#     title = "Обновления Yatube"
#     context = {
#         'title_index': title
#     }
#     return render(request, template, context)

def index(request):
    template = 'posts/index.html'
    posts = Post.objects.order_by('-pub_date')[:10]
    context = {
        'posts' : posts,
    }
    return render(request, template, context)  

def group_list(request):
    template = 'posts/group_list.html'
    title = "Здесь будет информация о группах проекта Yatube"
    context = {
        'title': title
    }
    return render(request, template, context)

def group_posts(request, slug):
    return HttpResponse(f'Это пост группы: "{slug}"')







