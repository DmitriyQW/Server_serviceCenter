from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView,TokenVerifyView

from .serializers import UserOrdersSerializer
from .views import UserCreateView, ManufacturerApplic, UserRegisterView, MasterListView, UserListView, \
    ApplicationCreateView, StateApplicList, TypeDeviceList, ManufacturerList, PriceListView, OrderListView, \
    UserProfileView, UserOrdersView, CompleteOrderAPIView, PasswordResetByQuestionView

#Обработка адресов
urlpatterns = [
    path('',views.index), #Главная страница сервисного центра
    # path('pricelist/',views.pricelist),#127.0.0.1:8000/pricelist
    # path('counter/<int:id_count>/',views.counter),#127.0.0.1:8000/counter


    #api

    # Сброс пароля
    path('api/v1/recovery-password/', PasswordResetByQuestionView.as_view(), name='recovery-password'),
    # http://127.0.0.1:8000/api/v1/recovery-password/

    #Регистрация нового пользователя
    path('api/v1/users-register-2/', UserRegisterView.as_view(), name='user-register'), ####
    #http://127.0.0.1:8000/api/v1/users-register-2/

    # Авторизация
    path('api/v1/user-sign/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # http://127.0.0.1:8000/api/v1/user-sign/

    # Обновление токина
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # http://127.0.0.1:8000/api/v1/token/refresh/



    # Мастера и пользователи
    path('api/v1/masters/', MasterListView.as_view(), name='list-masters'),  # api возвращающие всех мастеров
    # http://127.0.0.1:8000/api/v1/masters/

    path('api/v1/users/', UserListView.as_view(), name='list-users'),  # api возвращающие всех пользователей
    # http://127.0.0.1:8000/api/v1/users/


    #Взятие для создание заказа

    #Статус заявки (Уточнение информации)
    path('api/v1/states-applic/', StateApplicList.as_view(), name='states-list'),
    # http://127.0.0.1:8000/api/v1/states-applic/

    #Тип устройства (Планшет)
    path('api/v1/type-devices-applic/', TypeDeviceList.as_view(), name='devices-list'),
    # http://127.0.0.1:8000/api/v1/type-devices-applic/

    #Производитель (Xiaomi)
    path('api/v1/manufacturers-applic/', ManufacturerList.as_view(), name='manufacturers-list'),
    # http://127.0.0.1:8000/api/v1/manufacturers-applic/

    #Создание заказа
    path('api/v1/orders/create/', ApplicationCreateView.as_view(), name='create-order'),
    # http://127.0.0.1:8000/api/v1/orders/create/

    #Для вывода данных о профиле пользователя по токену
    path('api/v1/user-profile/', UserProfileView.as_view(), name='user-profile'),
    # http://127.0.0.1:8000/api/v1/user-profile/

    # Возвращаем список всех заказов пользователя
    path('api/v1/user-orders/',UserOrdersView.as_view(),name='user-orders'),
    # http://127.0.0.1:8000/api/v1/user-orders/

    #Прайс лист

    path('api/v1/pricelist/', PriceListView.as_view(), name='pricelist'),
    # http://127.0.0.1:8000/api/v1/pricelist/



    #Для мастера
    #Вывод всех заказов
    path('api/v1/master-orders/', OrderListView.as_view(), name='order-list'),
    # http://127.0.0.1:8000/api/v1/master-orders/


    #Обновление статуса заявки для мастера
    path('api/v1/orders/<int:order_id>/status/', views.UpdateOrderStatusAPIView.as_view(), name='update_order_status'),
    # http://127.0.0.1:8000/api/v1/orders/1/status/

    #Завершение заказа мастером
    path('api/v1/orders/<int:pk>/complete/', CompleteOrderAPIView.as_view(), name='complete_order'),
    # http://127.0.0.1:8000/api/v1/orders/1/complete/


    # Не используется

    # path('api/v1/users-register/', UserCreateView.as_view(), name='user-create'),
    # #http://127.0.0.1:8000/api/v1/users-register/

    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]


