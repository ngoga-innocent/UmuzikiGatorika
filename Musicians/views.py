from django.shortcuts import render
from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Accounts.views import TokenVerification
from Accounts.serializers import UserSerializer
from .serializers import MusicianSerializer,MusicSkillSerializer
from .models import MusicianModel,MusicSkillChoices
# Create your views here.
class MusicianView(APIView):
    def get(self, request):
        # auth_token=request.META.get('HTTP_AUTHORIZATION')
        # user = TokenVerification(auth_token)

        # if not user:
        #     return Response({'error': 'Invalid token or unauthorized access'}, status=status.HTTP_401_UNAUTHORIZED)
        allmusician=MusicianModel.objects.all()
        serializer=MusicianSerializer(allmusician,many=True,context={"request":request})
        # user_serializer=UserSerializer(user,context={"request":request})
        return Response({'musician':serializer.data})
    
    def post(self,request):
        try:
            auth_token=request.META.get('HTTP_AUTHORIZATION')
            user = TokenVerification(auth_token)

            if not user:
                return Response({'detail': 'Invalid token or unauthorized access'}, status=status.HTTP_401_UNAUTHORIZED)
            
            serializer = MusicianSerializer(data={**request.data, 'user': user.id}) 
            if serializer.is_valid():
                serializer.save()
                return Response({'detail':'Musician created',
                                 'musician':serializer.data},status=status.HTTP_201_CREATED)
            else:
                return Response({'detail':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            print(e)
            # logger.exception("An error occurred while processing the request: %s", str(e))
            print(e)
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def put(self,request):
        try:
            auth_token=request.META.get('HTTP_AUTHORIZATION')
            user = TokenVerification(auth_token)
            if not user:
                return Response({'detail':'Please Login'})
            try:
                musician=MusicianModel.objects.get(user=user.id)
                serializer=MusicianSerializer(musician,request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'musician':serializer.data},status=status.HTTP_200_OK)
                else:
                    return Response({"detail":serializer.errors},status=400)
            except MusicianModel.DoesNotExist:
                return Response({"detail":'no Musician of this account Available'},status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"detail":'failed to update please try again'},status=status.HTTP_400_BAD_REQUEST)

class MusicalSkills(APIView):
    def get(self,request):
        all_skills=MusicSkillChoices.objects.all()
        serializer=MusicSkillSerializer(all_skills,many=True)
        return Response({'skills':serializer.data})

        
        