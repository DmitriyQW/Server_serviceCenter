from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView,TokenVerifyView
from .views import UserCreateView, ManufacturerApplic, UserRegisterView

#Обработка адресов
urlpatterns = [
    path('',views.index), #Главная страница сервисного центра
    path('pricelist/',views.pricelist),#127.0.0.1:8000/pricelist
    path('counter/<int:id_count>/',views.counter),#127.0.0.1:8000/counter

    #api
    path('api/v1/users-register-2/', UserRegisterView.as_view(), name='user-register'), ####
    #http://127.0.0.1:8000/api/v1/users-register-2/

    # path('api/v1/users-register/', UserCreateView.as_view(), name='user-create'),
    # #http://127.0.0.1:8000/api/v1/users-register/

    # api
    path('api/v1/manufacturerapplic/', ManufacturerApplic.as_view(), name='get-manufacturerapplic'),
    # http://127.0.0.1:8000/api/v1/manufacturerapplic/

    # Эндпоинты для токенов
    path('api/v1/user-sign/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #http://127.0.0.1:8000/api/v1/user-sign/

    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]


