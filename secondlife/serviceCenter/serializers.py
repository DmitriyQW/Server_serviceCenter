from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer # Токины
from django.contrib.auth.hashers import  make_password
from serviceCenter.models import State_applic, TypeDevice_applic, Manufacturer_applic, Application, \
    PriceList, Feedbackcol_number, Feedback, Publications, CustomUser
from django.db.models import Q

#Сереализатор для формирования объектов и перевода в Json формат
# Для создания записи в бд
# Для изменения записи в бд содержимого полей объекта
# Для удаления записи в бд объекта


class PasswordResetByQuestionSerializer(serializers.Serializer):
    username = serializers.CharField(required=False) #Имя пользователя не обязательно
    answer = serializers.CharField(required=False) #Ответ на вопрос не обязательно
    new_password = serializers.CharField(required=False, min_length=8) #Новый пароль не обязательно минимальная длина 8

    def validate(self, data):
        stage = self.context.get('stage') # Текущая стадия
        username = data.get('username') # Получаем имя пользователя

        if stage == 'get_question': # Если получаем контрольный вопрос
            if not username: #Если не было имя пользователя
                raise serializers.ValidationError("Укажите username.")
            try:
                user = CustomUser.objects.get(username=username) #Ищем пользователя в бд
            except CustomUser.DoesNotExist: #Если не найден пользователь
                raise serializers.ValidationError("Пользователь не найден.")
            data['question'] = user.question # Добавляем вопрос в данные
            return data # Возвращаем данные

        elif stage == 'check_answer': #Стадия проверка ответа
            if not username or not data.get('answer'): #Если не указан пароль или ответ на вопрос
                raise serializers.ValidationError("Укажите username и ответ.")
            try: #Пробуем найти пользователя
                user = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist: #Пользователь не найден
                raise serializers.ValidationError("Пользователь не найден.")
            if not user.check_answer(data['answer']): #Не верный ответ
                raise serializers.ValidationError("Неверный ответ на контрольный вопрос.")
            return data

        elif stage == 'set_password': #Стадия смены пароля
            if not username or not data.get('answer') or not data.get('new_password'): #Если что либо не передано username,ответ,новый,пароль
                raise serializers.ValidationError("Укажите username, ответ и новый пароль.")
            try: #Поиск пользователя
                user = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError("Пользователь не найден.")
            if not user.check_answer(data['answer']):#Проверка контрольного ответа
                raise serializers.ValidationError("Неверный ответ на контрольный вопрос.")
            data['user'] = user
            return data

        else: #Если не передана стадия
            raise serializers.ValidationError("Неизвестная стадия запроса.")

    def save(self):
        user = self.validated_data['user']  # Получаем пользователя
        user.set_password(self.validated_data['new_password'])  # Меняем на новый пароль
        user.save() #Сохраняем пользователя
        return user


class CompleteOrderSerializer(serializers.ModelSerializer): #Сериализация для завершения заказа
    deviceStatus_applic = serializers.CharField() #Описания состояния устройства
    descriptionWorks_applic = serializers.CharField() #Описания выполненных работ
    verdictPrice_applic = serializers.CharField() #Описания стоимости выполненных работ
    totalAmount = serializers.FloatField() #Общая стоимость

    class Meta:
        model = Application  # Модель, с которой работает сериализатор
        fields = [ # Список полей, которые будут сериализованы
            'deviceStatus_applic',
            'descriptionWorks_applic',
            'verdictPrice_applic',
            'totalAmount',
        ]

    def update(self, instance, validated_data):
        # Заполняем поля из профиля мастера
        instance.id_worker_applic = self.context['request'].user  # ID мастера
        instance.adresssamoviz_applic = self.context['request'].user.address  # Адрес мастера
        instance.telmastersamoviz_applic = self.context['request'].user.tel  # Телефон мастера
        instance.fiomastersamoviz_applic = self.context['request'].user.fio  # ФИО мастера

        # Заполняем поля из запроса

        # Обновляем описания состояния устройства
        instance.deviceStatus_applic = validated_data.get('deviceStatus_applic', instance.deviceStatus_applic)
        # Обновляем описания выполненных работ
        instance.descriptionWorks_applic = validated_data.get('descriptionWorks_applic',
                                                              instance.descriptionWorks_applic)
        # Обновляем описания стоимости выполненных работ
        instance.verdictPrice_applic = validated_data.get('verdictPrice_applic', instance.verdictPrice_applic)
        # Обновляем общую стоимость
        instance.totalAmount = validated_data.get('totalAmount', instance.totalAmount)

        instance.save() # Сохраняем изменения в базе данных
        return instance # Возвращаем обновленный экземпляр


class UserOrdersSerializer(serializers.ModelSerializer): # Сереализатор для возвращения всех заказов пользователя
    numberOrder = serializers.CharField(source='id_application') #id заказа
    dataOrder = serializers.CharField(source='date_applic') #Дата создания
    statusOrder = serializers.CharField(source='id_state_applic.name_state') # Статус заявки
    fioMasterOrder = serializers.CharField(source='fiomastersamoviz_applic', allow_null=True)# Фио мастера
    telMasterOrder = serializers.CharField(source='telmastersamoviz_applic', allow_null=True)# Телефон мастера
    adressMasterOrder = serializers.CharField(source='adresssamoviz_applic', allow_null=True)# Адрес мастера
    reasonApplicOrder = serializers.CharField(source='reason_applic') #Причина обращения
    typeDeviceOrder = serializers.CharField(source='id_typeDevice_applic.name_typeD') #Тип устройства
    manufacturerOrder = serializers.CharField(source='id_manufacturer_applic.name_manufacturer') #Производитель
    modelOrder = serializers.CharField(source='model_applic') # Модель устройства
    descriptionWorkMasterOrder = serializers.CharField(source='descriptionWorks_applic', allow_null=True) #Описание выполненных работ
    descriptionPriceMasterOrder = serializers.CharField(source='verdictPrice_applic', allow_null=True)#Какая услуга сколько стоит
    totalAmount = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True)#Итоговая стоимость

    class Meta:
        model = Application #Модель
        fields = [ #Поля для сереализации
            'numberOrder',
            'dataOrder',
            'statusOrder',
            'fioMasterOrder',
            'telMasterOrder',
            'adressMasterOrder',
            'reasonApplicOrder',
            'typeDeviceOrder',
            'manufacturerOrder',
            'modelOrder',
            'descriptionWorkMasterOrder',
            'descriptionPriceMasterOrder',
            'totalAmount'
        ]


class UserProfileSerializer(serializers.ModelSerializer):  #Сериализатор для данных пользователя
    loginUser = serializers.CharField(source='username')  # Поле "loginUser" берет данные из "username" модели
    fioUser = serializers.CharField(source='fio')
    emailUser = serializers.CharField(source='email')
    telUser = serializers.CharField(source='tel')
    adressUser = serializers.CharField(source='address')

    class Meta:
        model = CustomUser # Указываем модель, с которой работает сериализатор
        fields = ['loginUser', 'fioUser', 'emailUser', 'telUser', 'adressUser'] # Список полей для сериализации


class OrderItemSerializer(serializers.ModelSerializer): #Сереализатор Заказов для отображения мастеру
    # Шапка
    numberOrder = serializers.CharField(source='id_application')
    dataOrder = serializers.DateTimeField(source='date_applic')
    steteOrder = serializers.CharField(source='id_state_applic.name_state')

    # Описание
    reasonApplicOrder = serializers.CharField(source='reason_applic')
    historyOrder = serializers.CharField(source='history_applic')
    otherInfoOrder = serializers.CharField(source='otherInfo_applic')

    # Об устройстве (исправлено source для связанных моделей)
    typeDeviceOrder = serializers.CharField(source='id_typeDevice_applic.name_typeD')
    manufacturerOrder = serializers.CharField(source='id_manufacturer_applic.name_manufacturer')
    modelOrder = serializers.CharField(source='model_applic')

    # Контакты
    fioUserOrder = serializers.CharField(source='user_fio_applic')
    telUserOrder = serializers.CharField(source='user_tel_applic')
    emailUserOrder = serializers.CharField(source='user_email_applic')
    adressUserOrder = serializers.CharField(source='user_adress_applic')

    class Meta:
        model = Application # Указываем модель Заказа
        fields = [
            'numberOrder', 'dataOrder', 'steteOrder',
            'reasonApplicOrder', 'historyOrder', 'otherInfoOrder',
            'typeDeviceOrder', 'manufacturerOrder', 'modelOrder',
            'fioUserOrder', 'telUserOrder', 'emailUserOrder', 'adressUserOrder'
        ]  # Список полей, которые будут сериализованы


class ApplicationCreateSerializer(serializers.ModelSerializer): #Создание заказа для пользователя
    class Meta:
        model = Application  # Указываем модель, с которой работает сериализатор
        fields = [
            'id_typeDevice_applic',
            'id_manufacturer_applic',
            'model_applic',
            'reason_applic',
            'history_applic',
            'passwordDevice_applic',
            'otherInfo_applic',
        ]

    exclude = ['deviceStatus_applic'] # Поля, которые будут исключены из сериализации (в данном случае это поле deviceStatus_applic)

    def create(self, request, validated_data):
        user = request.user # Получаем текущего аутентифицированного пользователя из запроса
        state_applic_new = State_applic.objects.get(pk=2) # Получаем объект статуса заявки с id=2 ("Уточнение информации")

        # Создаем новую заявку, используя данные из validated_data и информацию о пользователе
        application = Application.objects.create(
            id_user_applic=user,
            id_state_applic=state_applic_new,
            user_fio_applic=user.fio,
            user_tel_applic=user.tel,
            user_email_applic=user.email,
            user_adress_applic=user.address,
            **validated_data # Остальные данные, переданные в запросе
        )
        # Возвращаем созданную заявку
        return application



class UserRegisterSerializer(serializers.ModelSerializer):
    ## Сериализатор для регистрации пользователя
    class Meta:
        model = CustomUser  # Модель
        fields = ['username', 'tel', 'email', 'password', 'question', 'answer', 'fio', 'address', 'age']
        extra_kwargs = {
            'password': {'write_only': True},
            'answer': {'write_only': True}
        }

    def validate(self, attrs): # Проверка что телефон или логин не заняты
        username = attrs.get('username')
        tel = attrs.get('tel')

        if CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': 'Данный username уже занят.'})

        if CustomUser.objects.filter(tel=tel).exists():
            raise serializers.ValidationError({'tel': 'Данный номер телефона уже занят.'})

        return attrs

    def create(self, validated_data):
        validated_data['user_type'] = 'user'  # Установите тип пользователя на "user"
        validated_data['password'] = make_password(validated_data['password'])  # Хеширование пароля
        validated_data['answer'] = make_password(validated_data['answer'])  # Хеширование ответа на вопрос
        return super().create(validated_data)


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



