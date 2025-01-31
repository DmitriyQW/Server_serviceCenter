from operator import index
from xml.etree.ElementInclude import include

from django.urls import path,include
from . import views, routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView,TokenVerifyView
from .views import CustomTokenObtainPairView,CustomTokenRefreshView


#Обработка адресов
urlpatterns = [
    path('',views.index), #Главная страница сервисного центра
    path('pricelist/',views.pricelist),#127.0.0.1:8000/pricelist
    path('counter/<int:id_count>/',views.counter),#127.0.0.1:8000/counter
    path('api/v1/',include(routers.urlsapi)),

    # Эндпоинты для токенов
    path('api/v1/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'), #http://127.0.0.1:8000/api/v1/token/
    path('api/v1/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'), #http://127.0.0.1:8000/api/v1/token/refresh/
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]


