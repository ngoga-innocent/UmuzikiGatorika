from rest_framework import serializers
from .models import Event,EventImage,TrendingSongs



class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model=Event
        fields='__all__'

class EventImageSerializer(serializers.ModelSerializer):
   
    class Meta:
        model=EventImage
        fields='__all__'
class TrendingSerializer(serializers.ModelSerializer):
    class Meta:
        model=TrendingSongs
        fields='__all__'