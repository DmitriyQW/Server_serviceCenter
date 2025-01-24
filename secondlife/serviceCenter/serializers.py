from typing import ReadOnly

from rest_framework import serializers

from serviceCenter.models import Worker, User


#Сереализатор для формирования объектов и перевода в Json формат
class WorkerSerializer(serializers.Serializer):
    id_worker = serializers.IntegerField()
    login_worker = serializers.CharField(max_length=32)
    tel_worker = serializers.CharField(max_length=11)
    email_worker = serializers.EmailField(max_length=254)
    password_worker = serializers.CharField(max_length=255)  # HES
    question_worker = serializers.CharField(max_length=100)
    answer_worker = serializers.CharField(max_length=255)
    fio_worker = serializers.CharField(max_length=110)
    address_worker = serializers.CharField(max_length=256)
    age_worker = serializers.IntegerField()
    dateregister_worker = serializers.DateTimeField()

    def create(self, validated_data):
        return Worker.objects.create(**validated_data)


class UserSerializer(serializers.Serializer):
    id_user = serializers.IntegerField(read_only=True)
    login_user = serializers.CharField(max_length=32)
    tel_user = serializers.CharField(max_length=11)
    email_user = serializers.EmailField(max_length=254)
    password_user = serializers.CharField(max_length=255)  # HES
    question_user = serializers.CharField(max_length=100)
    answer_user = serializers.CharField(max_length=255) # HES
    fio_user = serializers.CharField(max_length=110)
    address_user = serializers.CharField(max_length=256)
    age_user = serializers.IntegerField()
    dateregister_user = serializers.DateTimeField(read_only=True) #read_only=True надо добавить если пытаться изменить запись

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.login_user = instance.login_user
        instance.tel_user = validated_data.get("tel_user", instance.tel_user)
        instance.email_user = validated_data.get("email_user", instance.email_user)
        instance.password_user = validated_data.get("password_user", instance.password_user)
        instance.question_user = validated_data.get("question_user", instance.question_user)
        instance.answer_user = validated_data.get("answer_user", instance.answer_user)
        instance.fio_user = validated_data.get("fio_user", instance.fio_user)
        instance.address_user = validated_data.get("address_user", instance.address_user)
        instance.age_user = validated_data.get("age_user", instance.age_user)
        instance.save()
        return  instance

class State_applicSerializer(serializers.Serializer):
    id_state = serializers.IntegerField()
    name_state = serializers.CharField(max_length=100)

class TypeDevice_applicSerializer(serializers.Serializer):
    id_typeD = serializers.IntegerField()
    name_typeD = serializers.CharField(max_length=100)

class Manufacturer_applicSerializer(serializers.Serializer):
    id_manufacturer = serializers.IntegerField()
    name_manufacturer = serializers.CharField(max_length=100)

class ApplicationSerializer(serializers.Serializer):
    id_application = serializers.IntegerField()
    id_state_applic = serializers.IntegerField()  # Статус заявки (Готово)
    id_user_applic = serializers.IntegerField()
    id_worker_applic = serializers.IntegerField()  # NULL
    photo_applic = serializers.CharField(max_length=200)
    id_typeDevice_applic = serializers.IntegerField()  # Тип устройства (Планшет)
    id_manufacturer_applic = serializers.IntegerField()
    model_applic = serializers.CharField(max_length=100)
    reason_applic = serializers.CharField(max_length=250)
    history_applic = serializers.CharField(max_length=500)
    passwordDevice_applic = serializers.CharField(max_length=256)
    otherInfo_applic = serializers.CharField(max_length=1000)
    date_applic = serializers.DateTimeField()
    deviceStatus_applic = serializers.CharField(max_length=1000)  # Состояние Устройства (Рабочий, Не рабочий,скол и т.п)
    adresssamoviz_applic = serializers.CharField(max_length=256)  # Null
    telmastersamoviz_applic = serializers.CharField(max_length=11)  # Null
    fiomastersamoviz_applic = serializers.CharField(max_length=110)  # Null
    # Дефект пользователя reason_applic
    descriptionWorks_applic = serializers.CharField(max_length=2000)  # Null
    verdictPrice_applic = serializers.CharField(max_length=2000)  # Null

class PriceListSerializer(serializers.Serializer):
    id_service = serializers.IntegerField()
    name_service = serializers.CharField(max_length=100)
    description_service = serializers.CharField(max_length=500)
    price_service = serializers.DecimalField(max_digits=10, decimal_places=2)

class ReportSerializer(serializers.Serializer):
    id_Report = serializers.IntegerField()
    login = serializers.CharField(max_length=32)
    ip = serializers.CharField(max_length=20)
    device = serializers.CharField(max_length=100)
    action = serializers.CharField(max_length=100)
    date_action = serializers.DateTimeField()

class Feedbackcol_numberSerializer(serializers.Serializer):
    id_feedbackcol_number = serializers.IntegerField()
    number = serializers.IntegerField()

class FeedbackSerializer(serializers.Serializer):
    id_feedback = serializers.IntegerField()
    id_user = serializers.IntegerField()
    id_feedbackcol_number = serializers.IntegerField()
    description_service = serializers.CharField(max_length=500)
    date_feedback = serializers.DateTimeField()

class PublicationsSerializer(serializers.Serializer):
    id_publ = serializers.IntegerField()
    id_worker_public = serializers.IntegerField()
    photo_publ = serializers.CharField(max_length=200)
    description_publ = serializers.CharField(max_length=100)
    source_public = serializers.CharField(max_length=1000)
    date_public = serializers.DateTimeField()

class ChatSerializer(serializers.Serializer):
    id_chat = serializers.IntegerField()
    master_chat = serializers.IntegerField()
    user_chat = serializers.IntegerField()
    date_chat = serializers.DateTimeField()
    message_chat = serializers.CharField()