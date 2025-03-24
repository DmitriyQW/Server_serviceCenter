from django.http import HttpResponse
# Ответы на запросы.
from rest_framework import generics, status
from rest_framework.views import APIView

# Импорт моделей.
from .models import CustomUser, Manufacturer_applic, State_applic, TypeDevice_applic
from .permissions import IsUserOrAdmin
from .serializers import CustomUserSerializer, Manufacturer_applicSerializer, UserRegisterSerializer, \
    ApplicationCreateSerializer, TypeDevice_applicSerializer, State_applicSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated,AllowAny
from rest_framework.response import Response



# Ответы на запросы.



def index(request):
    return HttpResponse("Страница приложения сервисный центр")

def pricelist(request):
    return HttpResponse("<h1>Прайс лист</h1>")

def counter(request,id_count):
    return  HttpResponse(f"<h2>Х2 counter = {id_count}</h2>")


class ApplicationCreateView(APIView): #Создание заявки от пользователя и администратора
    permission_classes = [IsUserOrAdmin]

    def post(self, request):
        # Автоматическое заполнение полей
        data = request.data.copy()
        data['id_user_applic'] = request.user.id
        data['id_state_applic'] = 6  # Статус "Новая заявка"

        serializer = ApplicationCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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