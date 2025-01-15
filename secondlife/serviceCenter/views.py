from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

# Ответы на запросы.


def index(request):
    return HttpResponse("Страница приложения сервисный центр")

def pricelist(request):
    return HttpResponse("<h1>Прайс лист</h1>")

def counter(request,id_count):
    return  HttpResponse(f"<h2>Х2 counter = {id_count}</h2>")

# def page_not_found(request,exception):
#     return HttpResponseNotFound("<h1>Страница не найдена</h1>")