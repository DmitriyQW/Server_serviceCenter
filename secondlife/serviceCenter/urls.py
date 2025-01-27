from operator import index
from xml.etree.ElementInclude import include

from django.urls import path,include
from . import views
from .views import UsersViewSet, WorkerViewSet, ApplicationViewSet
from rest_framework import  routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView,TokenVerifyView
# from .views import ServiceCenterApiList, ServiceCenterUpdateAPIView

router = routers.SimpleRouter()
router.register(r'users',UsersViewSet)

routerWorker = routers.SimpleRouter()
routerWorker.register(r'workers',WorkerViewSet)

routerApplication = routers.SimpleRouter()
routerApplication.register(r'application',ApplicationViewSet)

#Обработка адресов
urlpatterns = [
    path('',views.index), #Главная страница сервисного центра
    path('pricelist/',views.pricelist),#127.0.0.1:8000/pricelist
    path('counter/<int:id_count>/',views.counter),#127.0.0.1:8000/counter
    path('api/v1/',include(router.urls)),  # 127.0.0.1:8000/api/v1/users/
    path('api/v1/',include(routerWorker.urls)),  # 127.0.0.1:8000/api/v1/works/
    path('api/v1/',include(routerApplication.urls)),  # 127.0.0.1:8000/api/v1/works/

    # path('api/v1/drf-auth/',include('rest_framework.urls')),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), #http://127.0.0.1:8000/api/v1/token/
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]


