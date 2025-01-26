from typing import ReadOnly

from rest_framework import serializers

from serviceCenter.models import Worker, User, State_applic, TypeDevice_applic, Manufacturer_applic, Application, \
    PriceList, Report, Feedbackcol_number, Feedback, Publications, Chat

#Сереализатор для формирования объектов и перевода в Json формат
# Для создания записи в бд
# Для изменения записи в бд содержимого полей объекта
# Для удаления записи в бд объекта
class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = '__all__'
        extra_kwargs = {
            'password_worker':{'write_only':True},
            'id_worker':{'read_only':True}
        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {

            'id_user':{'read_only':True}
        }

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

