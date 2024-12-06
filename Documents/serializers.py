from rest_framework import serializers
from .models import Copies,SongType,SongCategory,Request
from Accounts.models import Users

class CopiesSerializer(serializers.ModelSerializer):
    document=serializers.FileField()
    # uploader=serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())
    class Meta:
        model=Copies
        fields='__all__'
        read_only_fields = ['uploader']
class SongTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=SongType
        fields='__all__'
class SongCategorySerializer(serializers.ModelSerializer):
    song_count = serializers.SerializerMethodField()
    class Meta:
        model=SongCategory
        fields=['id','name','song_count']
        extra_kwargs={'id': {'read_only': True}} 
    def get_song_count(self, obj):
        return Copies.objects.filter(part=obj).count()           
class RequestDocumentSerializer(serializers.ModelSerializer):
        class Meta:
            model=Request
            fields='__all__'