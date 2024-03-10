from django.shortcuts import HttpResponse

# Create your views here.
def index(request):    
    return HttpResponse('Главная страница YaTube')

def group_posts(request, slug):
    return HttpResponse(f'Это пост группы: "{slug}"')