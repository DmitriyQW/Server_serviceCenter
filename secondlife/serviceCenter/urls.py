from operator import index
from django.urls import path
from . import views
from .views import ServiceCenterApiView

#Обработка адресов
urlpatterns = [
    path('',views.index), #Главная страница сервисного центра
    path('pricelist/',views.pricelist),#127.0.0.1:8000/pricelist
    path('counter/<int:id_count>/',views.counter),#127.0.0.1:8000/counter
    path('api/v1/users/',ServiceCenterApiView.as_view()),#127.0.0.1:8000/api/v1/users/
    path('api/v1/users/<int:pk>/', ServiceCenterApiView.as_view())  # 127.0.0.1:8000/api/v1/users/2/
]


