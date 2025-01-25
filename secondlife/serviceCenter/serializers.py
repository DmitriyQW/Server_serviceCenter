from typing import ReadOnly

from rest_framework import serializers

from serviceCenter.models import Worker, User, State_applic, TypeDevice_applic, Manufacturer_applic, Application, \
    PriceList, Report, Feedbackcol_number, Feedback, Publications, Chat


#Сереализатор для формирования объектов и перевода в Json формат
class WorkerSerializer(serializers.Serializer):
    id_worker = serializers.IntegerField(read_only=True)
    login_worker = serializers.CharField(max_length=32)
    tel_worker = serializers.CharField(max_length=11)
    email_worker = serializers.EmailField(max_length=254)
    password_worker = serializers.CharField(max_length=255)  # HES
    question_worker = serializers.CharField(max_length=100)
    answer_worker = serializers.CharField(max_length=255)
    fio_worker = serializers.CharField(max_length=110)
    address_worker = serializers.CharField(max_length=256)
    age_worker = serializers.IntegerField()
    dateregister_worker = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Worker.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.login_worker = instance.login_worker  # Не низменный по типу id
        instance.tel_worker = validated_data.get("tel_worker", instance.tel_worker)
        instance.email_worker = validated_data.get("email_worker", instance.email_worker)
        instance.password_worker = validated_data.get("password_worker", instance.password_worker)
        instance.question_worker = validated_data.get("question_worker", instance.question_worker)
        instance.answer_worker = validated_data.get("answer_worker", instance.answer_worker)
        instance.fio_worker = validated_data.get("fio_worker", instance.fio_worker)
        instance.age_worker = validated_data.get("age_worker", instance.age_worker)
        instance.age_worker = validated_data.get("age_worker", instance.age_worker)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
        return instance

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
        instance.login_user = instance.login_user #Не низменный по типу id
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

    def delete(self, instance):
        instance.delete()
        return  instance

class State_applicSerializer(serializers.Serializer):
    id_state = serializers.IntegerField(read_only=True)
    name_state = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return State_applic.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name_state = validated_data.get("name_state",instance.name_state)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
        return  instance

class TypeDevice_applicSerializer(serializers.Serializer):
    id_typeD = serializers.IntegerField(read_only=True)
    name_typeD = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return TypeDevice_applic.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name_typeD = validated_data.get("name_typeD",instance.name_typeD)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
        return  instance

class Manufacturer_applicSerializer(serializers.Serializer):
    id_manufacturer = serializers.IntegerField(read_only=True)
    name_manufacturer = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Manufacturer_applic.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name_manufacturer = validated_data("name_manufacturer",instance.name_manufacturer)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
        return  instance

class ApplicationSerializer(serializers.Serializer): #Надо доделать
    id_application = serializers.IntegerField(read_only=True)
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
    date_applic = serializers.DateTimeField(read_only=True)
    deviceStatus_applic = serializers.CharField(max_length=1000)  # Состояние Устройства (Рабочий, Не рабочий,скол и т.п)
    adresssamoviz_applic = serializers.CharField(max_length=256)  # Null
    telmastersamoviz_applic = serializers.CharField(max_length=11)  # Null
    fiomastersamoviz_applic = serializers.CharField(max_length=110)  # Null
    # Дефект пользователя reason_applic
    descriptionWorks_applic = serializers.CharField(max_length=2000)  # Null
    verdictPrice_applic = serializers.CharField(max_length=2000)  # Null

    def create(self, validated_data):
        return Application.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id_state_applic = validated_data("id_state_applic",instance.id_state_applic)
        instance.id_user_applic = validated_data("id_user_applic", instance.id_user_applic)
        instance.id_worker_applic = validated_data("id_worker_applic", instance.id_worker_applic)
        instance.photo_applic = validated_data("photo_applic", instance.photo_applic) # Не понятно
        instance.id_typeDevice_applic = validated_data("id_typeDevice_applic", instance.id_typeDevice_applic)
        instance.id_manufacturer_applic = validated_data("id_manufacturer_applic", instance.id_manufacturer_applic)
        instance.model_applic = validated_data("model_applic", instance.model_applic)
        instance.reason_applic = validated_data("reason_applic", instance.reason_applic)
        instance.history_applic = validated_data("history_applic", instance.history_applic)
        instance.passwordDevice_applic = validated_data("passwordDevice_applic", instance.passwordDevice_applic)
        instance.otherInfo_applic = validated_data("otherInfo_applic", instance.otherInfo_applic)
        instance.deviceStatus_applic = validated_data("deviceStatus_applic", instance.deviceStatus_applic)
        instance.adresssamoviz_applic = validated_data("adresssamoviz_applic", instance.adresssamoviz_applic)
        instance.telmastersamoviz_applic = validated_data("telmastersamoviz_applic", instance.telmastersamoviz_applic)
        instance.fiomastersamoviz_applic = validated_data("fiomastersamoviz_applic", instance.fiomastersamoviz_applic)
        instance.descriptionWorks_applic = validated_data("descriptionWorks_applic", instance.descriptionWorks_applic)
        instance.verdictPrice_applic = validated_data("verdictPrice_applic", instance.verdictPrice_applic)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
        return  instance

class PriceListSerializer(serializers.Serializer):
    id_service = serializers.IntegerField(read_only=True)
    name_service = serializers.CharField(max_length=100)
    description_service = serializers.CharField(max_length=500)
    price_service = serializers.DecimalField(max_digits=10, decimal_places=2)

    def create(self, validated_data):
        return PriceList.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name_service = validated_data.get("name_service",instance.name_service)
        instance.description_service = validated_data.get("description_service", instance.description_service)
        instance.price_service = validated_data.get("price_service", instance.price_service)
        instance.save()
        return  instance

    def delete(self, instance):
        instance.delete()
        return  instance

class ReportSerializer(serializers.Serializer):
    id_Report = serializers.IntegerField(read_only=True)
    login = serializers.CharField(max_length=32)
    ip = serializers.CharField(max_length=20)
    device = serializers.CharField(max_length=100)
    action = serializers.CharField(max_length=100)
    date_action = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Report.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.login = validated_data.get("login",instance.login)
        instance.ip = validated_data.get("ip", instance.ip)
        instance.device = validated_data.get("device", instance.device)
        instance.action = validated_data.get("action", instance.action)
        instance.save()
        return  instance

    def delete(self, instance):
        instance.delete()
        return instance

class Feedbackcol_numberSerializer(serializers.Serializer):
    id_feedbackcol_number = serializers.IntegerField(read_only=True)
    number = serializers.IntegerField()

    def create(self, validated_data):
        return Feedbackcol_number.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.number = validated_data.get("number",instance.number)
        instance.save()
        return  instance

    def delete(self, instance):
        instance.delete()
        return instance

class FeedbackSerializer(serializers.Serializer):
    id_feedback = serializers.IntegerField(read_only=True)
    id_user = serializers.IntegerField()
    id_feedbackcol_number = serializers.IntegerField()
    description_service = serializers.CharField(max_length=500)
    date_feedback = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Feedback.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id_user = validated_data.get("id_user",instance.id_user)
        instance.id_feedbackcol_number = validated_data.get("id_feedbackcol_number", instance.id_feedbackcol_number)
        instance.description_service = validated_data.get("description_service", instance.description_service)
        instance.save()
        return  instance

    def delete(self, instance):
        instance.delete()
        return instance

class PublicationsSerializer(serializers.Serializer):
    id_publ = serializers.IntegerField(read_only=True)
    id_worker_public = serializers.IntegerField()
    photo_publ = serializers.CharField(max_length=200)
    description_publ = serializers.CharField(max_length=100)
    source_public = serializers.CharField(max_length=1000)
    date_public = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Publications.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id_worker_public = validated_data.get("id_worker_public",instance.id_worker_public)
        instance.photo_publ = validated_data.get("photo_publ", instance.photo_publ)
        instance.description_publ = validated_data.get("description_publ", instance.description_publ)
        instance.source_public = validated_data.get("source_public", instance.source_public)
        instance.save()
        return  instance

    def delete(self, instance):
        instance.delete()
        return instance

class ChatSerializer(serializers.Serializer):
    id_chat = serializers.IntegerField(read_only=True)
    master_chat = serializers.IntegerField()
    user_chat = serializers.IntegerField()
    date_chat = serializers.DateTimeField(read_only=True)
    message_chat = serializers.CharField()

    def create(self, validated_data):
        return Chat.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.master_chat = validated_data.get("master_chat",instance.master_chat)
        instance.user_chat = validated_data.get("user_chat", instance.user_chat)
        instance.message_chat = validated_data.get("message_chat", instance.message_chat)
        instance.save()
        return  instance

    def delete(self, instance):
        instance.delete()
        return instance