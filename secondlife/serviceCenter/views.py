from django.http import HttpResponse
# Ответы на запросы.
from rest_framework import generics, status
from rest_framework.views import APIView

# Импорт моделей.
from .models import CustomUser, Manufacturer_applic, State_applic, TypeDevice_applic, PriceList, Application
from .permissions import IsUserOrAdmin, IsMasterOrAdmin
from .serializers import CustomUserSerializer, Manufacturer_applicSerializer, UserRegisterSerializer, \
    ApplicationCreateSerializer, TypeDevice_applicSerializer, State_applicSerializer, PriceListSerializer, \
    OrderItemSerializer, UserProfileSerializer, UserOrdersSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated,AllowAny
from rest_framework.response import Response



# Ответы на запросы.



def index(request):
    return HttpResponse("Страница приложения сервисный центр")

def pricelist(request):
    return HttpResponse("<h1>Прайс лист</h1>")

def counter(request,id_count):
    return  HttpResponse(f"<h2>Х2 counter = {id_count}</h2>")


class UserOrdersView(APIView): #Возвращаем список заказов пользователей
    permission_classes = [IsUserOrAdmin]  # Только для админа и пользователя

    def get(self, request):
        user = request.user  # Получаем текущего пользователя из токена
        user_orders = Application.objects.filter(id_user_applic=user)  # Фильтруем заказы по пользователю
        serializer = UserOrdersSerializer(user_orders, many=True)  # Сериализуем список заказов
        return Response(serializer.data)  # Возвращаем данные в формате JSON



class UserProfileView(APIView): #Возвращаем данные пользователя по токену
    permission_classes = [IsAuthenticated]  #Только для авторизированных пользователей

    def get(self, request):
        user = request.user #Получаем текущего пользователя из токена
        serializer = UserProfileSerializer(user) # Сериализуем данные пользователя
        return Response(serializer.data) # Возвращаем данные в формате JSON



class OrderListView(generics.ListAPIView): #Все заявки для мастера
    queryset = Application.objects.all() #Все объекты
    serializer_class = OrderItemSerializer #Сериализатор
    permission_classes = [IsMasterOrAdmin] #Ограничение только мастер и админ


class ApplicationCreateView(generics.CreateAPIView):
    serializer_class = ApplicationCreateSerializer # Указываем сериализатор, который будет использоваться для обработки данных
    permission_classes = [IsUserOrAdmin]  # Только пользователь или Admin

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  # Передаем данные из запроса в сериализатор
        serializer.is_valid(raise_exception=True)  # Проверяем данные на валидность. Если данные некорректны, выбрасывается исключение с ошибками.

        application = serializer.create(request, serializer.validated_data) # Вызываем метод `create` из сериализатора, передавая `request` и валидированные данные.
        headers = self.get_success_headers(serializer.data) # Получаем заголовки для успешного ответа

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)   # Возвращаем успешный ответ с данными созданной заявки и статусом HTTP 201 (Created)


# Справочники для анкеты
class StateApplicList(generics.ListAPIView): #Вывод всех статусов заявки
    queryset = State_applic.objects.all()
    serializer_class = State_applicSerializer
    permission_classes = [AllowAny]

class TypeDeviceList(generics.ListAPIView): #Вывод всех типов устройств
    queryset = TypeDevice_applic.objects.all()
    serializer_class = TypeDevice_applicSerializer
    permission_classes = [AllowAny]

class ManufacturerList(generics.ListAPIView): # Вывод всех производителей
    queryset = Manufacturer_applic.objects.all()
    serializer_class = Manufacturer_applicSerializer
    permission_classes = [AllowAny]

class PriceListView(generics.ListAPIView):
    queryset = PriceList.objects.all()
    serializer_class = PriceListSerializer
    permission_classes = [AllowAny]  # Прайс-лист доступен всем

class UserListView(generics.ListAPIView): ##
    """
    ListAPIView для просмотра списка всех пользователей.
    Доступен только администраторам.
    """
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        """
        Переопределяем метод get_queryset, чтобы возвращать только пользователей.
        """
        return CustomUser.objects.filter(user_type='user')


class MasterListView(generics.ListAPIView): ##
    """
    ListAPIView для просмотра списка всех мастеров.
    Доступен только администраторам.
    """
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        """
        Переопределяем метод get_queryset, чтобы возвращать только мастеров.
        """
        return CustomUser.objects.filter(user_type='master')




class UserRegisterView(generics.CreateAPIView): ## View для регистрации обычных пользователей
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]  # Разрешаем неавторизованным пользователям создавать аккаунты


class UserCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]  # Используем наше пользовательское разрешение

    def perform_create(self, serializer):
        user_type = self.request.data.get('user_type')

        # Проверка на создание мастера только администратором
        if user_type == 'master' and not self.request.user.is_staff:
            return Response({"error": "Только администратор может создать мастера."}, status=status.HTTP_403_FORBIDDEN)


        serializer.save()

class ManufacturerApplic(generics.ListAPIView):
    queryset = Manufacturer_applic.objects.all()
    serializer_class = Manufacturer_applicSerializer
    permission_classes = [AllowAny]