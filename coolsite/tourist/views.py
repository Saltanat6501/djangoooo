from django.http import HttpResponse,HttpResponseNotFound,Http404
from django.shortcuts import render, redirect

from .models import *

menu = [{'title': "Сайт туралы",'url_name': 'about'},
        {'title': "Қосу",'url_name': 'add_page'},
        {'title': "Кері байланыс", 'url_name': 'contact'},
        {'title': "Кіру", 'url_name': 'login'}
       ]

def index(request):
    posts=Tourist.objects.all()
    context={
        'posts': posts,
        'menu': menu,
        'title': 'Басты бет'
    }

    return render(request, 'tourist/index.html', context)

def about(request):
    return render(request, 'tourist/about.html', {'menu': menu, 'title': 'Сайт туралы'})

def addpage(request):
    return HttpResponse("қосу")

def contact(request):
    return HttpResponse("Кері байланыс")

def login(request):
    return HttpResponse("Кіру")

def pageNotFound(request,exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

def show_post(request,post_id):
    return HttpResponse(f"Отображение статьи с id = {post_id}")