from typing import ReadOnly

from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer # Токины
from django.contrib.auth.hashers import check_password

from serviceCenter.models import Worker, User, State_applic, TypeDevice_applic, Manufacturer_applic, Application, \
    PriceList, Report, Feedbackcol_number, Feedback, Publications, Chat
from django.db.models import Q

from serviceCenter.utils import hash_answer, hash_password


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    login_or_email_or_phone = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('login_or_email_or_phone')
        password = attrs.get('password')

        # Универсальный поиск пользователя
        user = self.find_user(username)

        # Проверка пользователя
        if not user:
            raise serializers.ValidationError('Пользователь не найден')

        # Проверка пароля
        if not self.check_user_password(user, password):
            raise serializers.ValidationError('Неверный пароль')

        # Создаем токены
        refresh = self.get_token(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def find_user(self, username):
        # Поиск в User
        user = User.objects.filter(
            Q(email_user=username) |
            Q(login_user=username) |
            Q(tel_user=username)
        ).first()

        # Если не нашли в User, ищем в Worker
        if not user:
            user = Worker.objects.filter(
                Q(email_worker=username) |
                Q(login_worker=username) |
                Q(tel_worker=username)
            ).first()

        return user

    def check_user_password(self, user, password):
        # Проверка пароля для разных моделей
        if hasattr(user, 'password_user'):
            return check_password(password, user.password_user)
        elif hasattr(user, 'password_worker'):
            return check_password(password, user.password_worker)

        return False

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Добавляем дополнительную информацию в токен
        if hasattr(user, 'id_user'):
            token['user_id'] = user.id_user
            token['user_type'] = 'user'
        elif hasattr(user, 'id_worker'):
            token['user_id'] = user.id_worker
            token['user_type'] = 'worker'

        return token


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        # Стандартная валидация refresh токена
        data = super().validate(attrs)

        # Возвращаем только новый access token
        return {
            'access': data['access']
        }
#Сереализатор для формирования объектов и перевода в Json формат
# Для создания записи в бд
# Для изменения записи в бд содержимого полей объекта
# Для удаления записи в бд объекта
class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = '__all__'
        extra_kwargs = {
            'id_worker':{'read_only':True},
            'is_staff': {'default': False}
            # 'password_worker': {'write_only': True},
            # 'answer_worker': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password_worker'] = hash_password(
            validated_data['password_worker']
        )
        validated_data['answer_worker'] = hash_answer(
            validated_data['answer_worker']
        )
        validated_data['is_staff'] = False
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Хеширование при обновлении, если изменены
        if 'password_worker' in validated_data:
            validated_data['password_worker'] = hash_password(
                validated_data['password_worker']
            )

        if 'answer_worker' in validated_data:
            validated_data['answer_worker'] = hash_answer(
                validated_data['answer_worker']
            )

        return super().update(instance, validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'id_user': {'read_only': True},
            'is_staff': {'default': False}
            # 'password_user': {'write_only': True},
            # 'answer_user': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password_user'] = hash_password(
            validated_data['password_user']
        )
        validated_data['answer_user'] = hash_answer(
            validated_data['answer_user']
        )
        validated_data['is_staff'] = False
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Хеширование при обновлении, если изменены
        if 'password_user' in validated_data:
            validated_data['password_user'] = hash_password(
                validated_data['password_user']
            )

        if 'answer_user' in validated_data:
            validated_data['answer_user'] = hash_answer(
                validated_data['answer_user']
            )

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

