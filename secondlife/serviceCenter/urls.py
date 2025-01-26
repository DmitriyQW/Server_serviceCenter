from operator import index
from xml.etree.ElementInclude import include

from django.urls import path,include
from . import views
from .views import UsersViewSet, WorkerViewSet
from rest_framework import  routers

# from .views import ServiceCenterApiList, ServiceCenterUpdateAPIView

router = routers.SimpleRouter()
router.register(r'users',UsersViewSet)

routerWorker = routers.SimpleRouter()
routerWorker.register(r'workers',WorkerViewSet)

#Обработка адресов
urlpatterns = [
    path('',views.index), #Главная страница сервисного центра
    path('pricelist/',views.pricelist),#127.0.0.1:8000/pricelist
    path('counter/<int:id_count>/',views.counter),#127.0.0.1:8000/counter
    path('api/v1/',include(router.urls)),  # 127.0.0.1:8000/api/v1/users/
    path('api/v1/',include(routerWorker.urls)),  # 127.0.0.1:8000/api/v1/works/
]


