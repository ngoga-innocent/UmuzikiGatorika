from rest_framework import serializers
from .models import NotificationModal,Device
class NotificationSeriazer(serializers.ModelSerializer):
    class Meta:
        model=NotificationModal
        fields='__all__'
class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Device
        fields='__all__'