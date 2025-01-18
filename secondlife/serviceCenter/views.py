from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

# Ответы на запросы.
from rest_framework import generics
# Импорт моделей.
from .models import Worker, Application, User
# Импорт сиализатора.
from .serializers import WorkerSerializer

from rest_framework.response import Response
from rest_framework.views import APIView

from django.forms.models import model_to_dict
# Ответы на запросы.
def index(request):
    return HttpResponse("Страница приложения сервисный центр")

def pricelist(request):
    return HttpResponse("<h1>Прайс лист</h1>")

def counter(request,id_count):
    return  HttpResponse(f"<h2>Х2 counter = {id_count}</h2>")

# def page_not_found(request,exception):
#     return HttpResponseNotFound("<h1>Страница не найдена</h1>")

# class ServiceCenterApiView(generics.ListAPIView):
#     queryset = Worker.objects.all()
#     serializer_class = WorkerSerializer

class ServiceCenterApiView(APIView):
    #Вывод всех пользователей
    def get(self,request):
        lst_users = User.objects.all().values()
        return Response({'users': list(lst_users)})

    #Создание нового пользователя
    def post(self,request):
        user_new = User.objects.create(
        login_user=request.data['login_user'],
        tel_user=request.data['tel_user'],
        email_user=request.data['email_user'],
        password_user=request.data['password_user'],
        question_user=request.data['question_user'],
        answer_user=request.data['answer_user'],
        fio_user=request.data['fio_user'],
        address_user=request.data['address_user'],
        age_user=request.data['age_user'],
        )
        return Response({'user':model_to_dict(user_new)})