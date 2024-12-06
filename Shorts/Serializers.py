from rest_framework import serializers
from .models import Like,Video,Comments
from Accounts.serializers import UserSerializer
class VideoSerializer(serializers.ModelSerializer):
    video=serializers.FileField()
    class Meta:
        model=Video
        fields='__all__'

        def create(self, validated_data):
        
            uploader = self.context['uploader'].id
            return Video.objects.create(uploader=uploader, **validated_data)
class LikeSerializer(serializers.ModelSerializer):
    liker = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model=Like
        fields='__all__'

    def create(self,validated_data):
            validated_data['liker'] = self.context['request']
           
            
            return Like.objects.create(**validated_data)
class CommentSerializer(serializers.ModelSerializer):
    user_data=UserSerializer(source='commenter',read_only=True)
    commenter=serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model=Comments
        fields=['id','commenter','comment','user_data']
    def create(self,validated_data):
         validated_data['commenter']=self.context['request']
         return Comments.objects.create(**validated_data)

         