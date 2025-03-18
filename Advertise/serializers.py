from rest_framework import serializers
from .models import Event,EventImage,TrendingSongs,Comments,Likes
from Accounts.serializers import UserSerializer

class CommentSerializer(serializers.ModelSerializer):
    user_data=UserSerializer(read_only=True,source='user')
    class Meta:
        model=Comments
        fields=['id', 'event', 'user','user_data', 'comment', 'created_at']
        extra_kwargs = {
            'event': {'required': False, 'write_only': True}  # Event is stored but not required in request
        }
class EventImageSerializer(serializers.ModelSerializer):
   
    class Meta:
        model=EventImage
        fields='__all__'
class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Likes
        fields='__all__'
    def create(self, validated_data):
        return Likes.objects.create(**validated_data)
class EventSerializer(serializers.ModelSerializer):
    event_comments = CommentSerializer(many=True, read_only=True)
    likes=LikesSerializer(many=True, read_only=True,source='event_like')
    like_count = serializers.SerializerMethodField()
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'thumbnail', 'location', 'date', 'created_at', 'likes','event_comments','like_count']
    def get_like_count(self, obj):
        return obj.event_like.count()

class TrendingSerializer(serializers.ModelSerializer):
    class Meta:
        model=TrendingSongs
        fields='__all__'