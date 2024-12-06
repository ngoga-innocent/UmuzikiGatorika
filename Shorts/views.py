from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Video,Like,Comments
from Accounts.views import TokenVerification
from .Serializers import VideoSerializer,LikeSerializer,CommentSerializer
# Create your views here.
class ShortsView(APIView):
    
    def get(self,request):
        videos=Video.objects.all()
        seriazer=VideoSerializer(videos,many=True,context={"request":request})
        return Response({"videos":seriazer.data})
    
    def post(self,request):
        auth_token=request.META.get('HTTP_AUTHORIZATION')
        user=TokenVerification(auth_token)
        if user:

            serializer=VideoSerializer(data=request.data,context={"uploader":user})
            if serializer.is_valid():
                serializer.save()
                return Response({"detail":"Posted"})
            else:
                return Response({"detail":serializer.errors})
        else:
            return Response({"detail":"Access Denied"},status=500)
    def delete(self,request):
        auth_token=request.META.get('HTTP_AUTHORIZATION')
        user=TokenVerification(auth_token)
        if not user:
            return Response({'detail':'User not found'})
        else:

            try:
                video=Video.objects.get(id=request.data['id'])
                if video.uploader==user:
                
                    video.delete()
                    return Response({"detail":"Video Deleted"})
                else:
                    return Response({"detail":"You are not Allowed to delete this video"})
            except Video.DoesNotExist:
                return Response({"detail":"Video not Found"})
class LikeView(APIView):
    def post(self,request):
        auth_token=request.META.get('HTTP_AUTHORIZATION')
        user=TokenVerification(auth_token)
        if not user:
            return Response({'detail':'User not found'})
        else:
            
            video=get_object_or_404(Video,id=request.data['video'])

            serializer=LikeSerializer(data=request.data,context={"request":user})
            if serializer.is_valid():
                serializer.save()
                video.Likes=request.data['likes']
                video.save()
                return Response({"detail":"Liked"})
            else:
                return Response({"detail":serializer.errors},status=401)
class CommentView(APIView):
    def get(self,request):
        video_id = request.query_params.get('video_id')
        if not video_id:
            return Response({"error": "Video ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        comments=Comments.objects.filter(video=video_id)
        seriazer=CommentSerializer(comments,many=True)
        return Response({"comments":seriazer.data},status=status.HTTP_200_OK)
    def post(self,request):
        auth_token=request.META.get('HTTP_AUTHORIZATION')
        user=TokenVerification(auth_token)
        if not user:
            return Response({'detail':'User not found'})
        else:
            try:
                video=get_object_or_404(Video,id=request.data['video'])
                serializer=CommentSerializer(data=request.data,context={"request":user})
                if serializer.is_valid():
                    serializer.save()
                    return Response({"detail":"comment saved"},status=200)
                else:
                    return Response({"detail":serializer.error_messages},status=401)
            except Video.DoesNotExist:
                return Response({"detail":"Video not found"},status=401)

