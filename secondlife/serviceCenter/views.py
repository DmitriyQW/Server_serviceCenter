from django.http import HttpResponse
from django.shortcuts import render

# Ответы на запросы.


def index(request):
    return HttpResponse("Страница приложения сервисный центр")

def pricelist(request):
    return HttpResponse("<h1>Прайс лист</h1>")