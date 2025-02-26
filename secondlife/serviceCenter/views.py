from django.http import HttpResponse
# Ответы на запросы.
from rest_framework import generics
# Импорт моделей.
from .models import CustomUser, Manufacturer_applic
from .serializers import CustomUserSerializer, Manufacturer_applicSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated,AllowAny
from rest_framework.response import Response



# Ответы на запросы.
def index(request):
    return HttpResponse("Страница приложения сервисный центр")

def pricelist(request):
    return HttpResponse("<h1>Прайс лист</h1>")

def counter(request,id_count):
    return  HttpResponse(f"<h2>Х2 counter = {id_count}</h2>")


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