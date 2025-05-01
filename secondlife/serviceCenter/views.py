from django.http import HttpResponse
# Ответы на запросы.
from rest_framework import generics, status
from rest_framework.views import APIView

from . import serializers
# Импорт моделей.
from .models import CustomUser, Manufacturer_applic, State_applic, TypeDevice_applic, PriceList, Application
from .permissions import IsUserOrAdmin, IsMasterOrAdmin
from .serializers import CustomUserSerializer, Manufacturer_applicSerializer, UserRegisterSerializer, \
    ApplicationCreateSerializer, TypeDevice_applicSerializer, State_applicSerializer, PriceListSerializer, \
    OrderItemSerializer, UserProfileSerializer, UserOrdersSerializer, CompleteOrderSerializer, \
    PasswordResetByQuestionSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated,AllowAny
from rest_framework.response import Response



# Ответы на запросы.



def index(request):
    return HttpResponse("Страница приложения сервисный центр")

def pricelist(request):
    return HttpResponse("<h1>Прайс лист</h1>")

def counter(request,id_count):
    return  HttpResponse(f"<h2>Х2 counter = {id_count}</h2>")

class PasswordResetByQuestionView(APIView):
    permission_classes = [AllowAny] #Для всех пользователей

    def post(self, request):
        stage = request.data.get('stage') # Стадия процесса из тела запроса
        serializer = PasswordResetByQuestionSerializer(data=request.data, context={'stage': stage})  #Сериализатор с передачей стадии  процесса

        # Проверка наличия стадии
        if not stage:
            return Response({'detail': 'Не указана стадия запроса.'}, status=status.HTTP_400_BAD_REQUEST)

        # Валидация данных
        if serializer.is_valid():
            # Логика для разных стадий
            if stage == 'get_question': #Получение контрольного вопроса
                return Response({'question': serializer.validated_data['question']}, status=status.HTTP_200_OK)
            elif stage == 'check_answer': #Проверка контрольного ответа
                return Response({'detail': 'Ответ верный. Теперь отправьте новый пароль.'}, status=status.HTTP_200_OK)
            elif stage == 'set_password': #Смена пароля
                serializer.save()
                return Response({'detail': 'Пароль успешно изменён.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Возврат ошибок валидации

class CompleteOrderAPIView(generics.UpdateAPIView):
    serializer_class = CompleteOrderSerializer # Класс сериализатора для завершения заказа
    permission_classes = [IsMasterOrAdmin]  # Права доступа для мастера и администратора
    queryset = Application.objects.all()  # Все заявки

    def get_object(self):  # Получение объекта заявки по ID
        order_id = self.kwargs['pk']
        try:
            return Application.objects.get(pk=order_id) # Попытка получить заявку по ID
        except Application.DoesNotExist: # Если заявка не найдена, вызываем ошибку валидации
            raise serializers.ValidationError("Заказ не найден.")

    # Обновление заявки
    def update(self, request, *args, **kwargs):
        instance = self.get_object()  # Получаем объект заявки
        serializer = self.get_serializer(instance, data=request.data, context={'request': request})  # Создаем сериализатор с передачей контекста запроса
        serializer.is_valid(raise_exception=True) # Проверяем валидность данных
        serializer.save() # Сохраняем изменения

        return Response(serializer.data)  # Возвращаем ответ с обновленными данными




class UpdateOrderStatusAPIView(APIView): #API для обновления статуса заявки
    permission_classes = [IsMasterOrAdmin] #Разрешение только для мастер и админа

    def patch(self, request, order_id): #Функция обновления принимает запрос и id заказа
        try:
            order = Application.objects.get(pk=order_id) #Получаем заказ по id
            new_status_id = request.data.get('status_id') #Получаем id статуса из запроса

            if not new_status_id: #Если статус не указан
                return Response({'error': 'status_id required'}, status=status.HTTP_400_BAD_REQUEST) #Возвращаем ошибку

            new_status = State_applic.objects.get(pk=new_status_id) #Получаем статус по id
            order.id_state_applic = new_status #Обновляем статус
            order.save() #Сохраняем изменения

            return Response({'message': 'Status updated'}) #Возвращаем сообщение об успехе
        except Application.DoesNotExist: #Если заказ не найден
            return Response({'error': 'Заказ не найден'}, status=status.HTTP_404_NOT_FOUND) #Возвращаем ошибку
        except State_applic.DoesNotExist: #Если статус не найден
            return Response({'error': 'Статус не найден'}, status=status.HTTP_400_BAD_REQUEST) #Возвращаем ошибку
        except Exception as e: #Если произошла другая ошибка
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) #Возвращаем ошибку



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