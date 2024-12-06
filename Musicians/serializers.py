from rest_framework import serializers
from .models import MusicianModel,MusicSkillChoices
from Accounts.serializers import UserSerializer

class MusicSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model=MusicSkillChoices
        fields='__all__'
class MusicianSerializer(serializers.ModelSerializer):
    user_data=UserSerializer(source='user', read_only=True)
    skills_data=MusicSkillSerializer(source='skills',many=True,read_only=True)
    class Meta:
        model=MusicianModel
        fields = ['id', 'user', 'user_data', 'skills','skills_data', 'description', 'recommended', 'location', 'phone_number', 'verified']

