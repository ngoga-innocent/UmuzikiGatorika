from django.shortcuts import render
from rest_framework.views import APIView
from .models import Event,EventImage,TrendingSongs,Likes
from .serializers import EventSerializer,EventImageSerializer,TrendingSerializer,CommentSerializer,LikesSerializer
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class Adverts(APIView):
    def get(self,request,id=None):
        event_id=request.GET.get('id',None)
        
        if event_id is not None:
            # print(f"Received event_id: {event_id}--{id}")
            try:
                event=Event.objects.get(id=event_id)
                # print(event)
                # event_images=EventImage.objects.filter(event=event_id)
                event_serializer=EventSerializer(event,context={'request':request})
                # print(event_serializer)
                # event_image_serializer=EventImageSerializer(event_images,context={"request":request},many=True)

                return Response({"event":event_serializer.data},status=status.HTTP_200_OK)
            except Event.DoesNotExist:
                return Response({"detail":'No event found'},status=404)
        else:
            one_month_ago = timezone.now() - timedelta(days=30)
            print(one_month_ago)
            event=Event.objects.filter(date__gte=one_month_ago).order_by("-created_at")[:70]
            
            serializer=EventSerializer(event,context={"request":request},many=True)
            # print(serializer.data)
            return Response({'events':serializer.data},status=status.HTTP_200_OK)
    def post(self,request):
        serializer=EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"response":serializer.data},status=status.HTTP_201_CREATED)
        else:
            return Response({"details":serializer.errors},status=status.HTTP_400_BAD_REQUEST)    
class Trending(APIView):
    def get(self,request):
        trending=TrendingSongs.objects.all().order_by('-created_at')
        serializer=TrendingSerializer(trending,context={'request':request},many=True)
        return Response({'trending':serializer.data},status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer=TrendingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"response":serializer.data},status=status.HTTP_201_CREATED)
        else:
            return Response({"details":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
class CommentView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        event_id=request.data.get('event_id',None)
        try:
            event=Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({"detail":'No event found'},status=404)    
        serializer=CommentSerializer(data=request.data)
        if serializer.is_valid():
            
            user=request.user
            serializer.save(event=event,user=user)
            return Response({"response":serializer.data},status=status.HTTP_201_CREATED)
        else:
            return Response({"details":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        try:
            event_id=request.data.get('event_id',None)
            print(f"Received event_id: {event_id}")
            event=Event.objects.get(id=event_id)
            comments=event.comments.all().order_by('-created_at')
            serializer=CommentSerializer(comments,context={'request':request},many=True)
            return Response({'comments':serializer.data},status=status.HTTP_200_OK)
        except Event.DoesNotExist:
            return Response({"detail":'No event found'},status=404)
class LikeView(APIView):
    def post(self,request):
        
        # print(request.data)
        
        event_id = request.data.get('event_id', None)
        device_token = request.data.get('device', None)

        if not event_id:
            return Response({"error": "Event ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            event = Event.objects.get(id=event_id)
            print(event)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the device has already liked this event
        if Likes.objects.filter(event=event, device=device_token).exists():
            return Response({"message": "Already liked"}, status=status.HTTP_200_OK)

        # Serialize and save the like
        # serializer = LikesSerializer(data=request.data)
        serializer = LikesSerializer(data={"event": event.id, "device": device_token})
        if serializer.is_valid():
            serializer.save()  # Make sure your serializer expects `event`
            return Response({"response": EventSerializer(event)}, status=status.HTTP_201_CREATED)

        print(serializer.errors)
        return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)