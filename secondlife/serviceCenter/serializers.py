from rest_framework import serializers

from serviceCenter.models import Worker


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ('id_worker','login_worker')