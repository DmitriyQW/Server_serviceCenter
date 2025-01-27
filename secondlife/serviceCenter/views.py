from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

# Ответы на запросы.
from rest_framework import generics,viewsets
# Импорт моделей.
from .models import Worker, Application, User
from .permissions import IsAdminOrReadOnly
# Импорт сиализатора.
from .serializers import WorkerSerializer, UserSerializer, ApplicationSerializer

from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
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

class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

#Api Workers только admin
class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
    permission_classes = (IsAdminUser,)

#Api Workers только admin
class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = (IsAuthenticated,)
    # permission_classes = (IsAdminOrReadOnly,)

