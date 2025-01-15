from operator import index
from django.urls import path
from . import views


#Обработка адресов
urlpatterns = [
    path('',views.index), #Главная страница сервисного центра
    path('pricelist/',views.pricelist),#127.0.0.1:8000/pricelist
    path('counter/<int:id_count>/',views.counter),#127.0.0.1:8000/counter
]


