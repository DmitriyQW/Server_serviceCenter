from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer # Токины
from django.contrib.auth.hashers import  make_password
from serviceCenter.models import State_applic, TypeDevice_applic, Manufacturer_applic, Application, \
    PriceList, Report, Feedbackcol_number, Feedback, Publications, Chat, CustomUser
from django.db.models import Q

#Сереализатор для формирования объектов и перевода в Json формат
# Для создания записи в бд
# Для изменения записи в бд содержимого полей объекта
# Для удаления записи в бд объекта


class UserRegisterSerializer(serializers.ModelSerializer):
    ## Сериализатор для регистрации пользователя
    class Meta:
        model = CustomUser #Модеель
        fields = ['username', 'tel', 'email', 'password', 'question', 'answer', 'fio', 'address', 'age']
        # Поля для сереализации
        extra_kwargs = {'password': {'write_only': True}, 'answer': {'write_only': True}}
        # Задание определённых свойств

    def create(self, validated_data):
        validated_data['user_type'] = 'user'  # Установите тип пользователя на "user"
        validated_data['password'] = make_password(validated_data['password'])  # Хеширование пароля
        validated_data['answer'] = make_password(validated_data['answer']) # Хеширование ответа на вопрос
        return super().create(validated_data) # Создание нового пользователя


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    login_or_email_or_phone = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('login_or_email_or_phone')
        password = attrs.get('password')

        user = self.find_user(username)

        if not user:
            raise serializers.ValidationError('Пользователь не найден')

        if not self.check_user_password(user, password):
            raise serializers.ValidationError('Неверный пароль')

        refresh = self.get_token(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'user_type': user.user_type,
            'fio': user.fio,
            'email': user.email,
        }

    def find_user(self, username):
        return CustomUser.objects.filter(
            Q(email=username) | Q(username=username) | Q(tel=username)
        ).first()

    def check_user_password(self, user, password):
        return user.check_password(password)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_id'] = user.id
        token['user_type'] = user.user_type
        return token

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        # Стандартная валидация refresh токена
        data = super().validate(attrs)

        # Возвращаем только новый access token
        return {
            'access': data['access']
        }

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    answer = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'username','tel','email','password','question', 'answer','fio', 'address',
            'age', 'user_type'
        ]

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['answer'] = make_password(validated_data['answer'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('password'):
            validated_data['password'] = make_password(validated_data['password'])

        if validated_data.get('answer'):
            validated_data['answer'] = make_password(validated_data['answer'])

        return super().update(instance, validated_data)


class State_applicSerializer(serializers.ModelSerializer):
    class Meta:
        model = State_applic
        fields = '__all__'
        extra_kwargs = {
            'id_state':{'read_only':True}
        }

class TypeDevice_applicSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeDevice_applic
        fields = '__all__'
        extra_kwargs = {
            'id_typeD':{'read_only':True}
        }

class Manufacturer_applicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer_applic
        fields = '__all__'
        extra_kwargs = {
            'id_manufacturer':{'read_only':True}
        }

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
        extra_kwargs = {
            'id_application':{'read_only':True},
            'date_applic':{'read_only':True}
        }

class PriceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceList
        fields = '__all__'
        extra_kwargs = {
            'id_service':{'read_only':True}
        }

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
        extra_kwargs = {
            'id_Report':{'read_only':True},
            'date_action': {'read_only': True}
        }

class Feedbackcol_numberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedbackcol_number
        fields = '__all__'
        extra_kwargs = {
            'id_feedbackcol_number':{'read_only':True}
        }

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
        extra_kwargs = {
            'id_feedback':{'read_only':True},
            'date_feedback': {'read_only': True}
        }

class PublicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publications
        fields = '__all__'
        extra_kwargs = {
            'id_publ':{'read_only':True},
            'date_public': {'read_only': True}
        }

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'
        extra_kwargs = {
            'id_chat':{'read_only':True},
            'date_chat': {'read_only': True}
        }

