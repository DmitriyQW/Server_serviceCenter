from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

# Ответы на запросы.
from rest_framework import generics
# Импорт моделей.
from .models import Worker, Application, User
# Импорт сиализатора.
from .serializers import WorkerSerializer, UserSerializer

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
        users = User.objects.all()
        return Response({'users': UserSerializer(users,many=True).data})

    #Создание нового пользователя
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        # Создание объекта сеореализатора и передача данных с запроса
        serializer.is_valid(raise_exception=True)
        # Проверка приходящего запроса
        # на полноту данных и соответствие ограничений полей
        serializer.save() # Сохранение записи
        return Response({'user':serializer.data}) #Вывод нового созданного пользователя

    def put(self,request,*args,**kwargs):
        pk = kwargs.get("pk",None)
        if not pk:
            return Response({"error":"Method PUT not allowed"})
        try:
            instance = User.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exist"})

        serializer = UserSerializer(data=request.data,instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return  Response({"user": serializer.data})

    def delete(self,request,**kwargs):
        pk = kwargs.get("pk",None)
        if not pk:
            return Response({"error":"Method Delete not allowed"})
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response({"user-delete": f"user-id:{pk} deleted"})
        except:
            return Response({"error": "Object does not exist"})

