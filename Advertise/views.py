from django.shortcuts import render
from rest_framework.views import APIView
from .models import Event,EventImage,TrendingSongs
from .serializers import EventSerializer,EventImageSerializer,TrendingSerializer
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta
from django.utils import timezone
# Create your views here.
class Adverts(APIView):
    def get(self,request):
        event_id=request.GET.get('id',None)
        
        if event_id is not None:
            print(f"Received event_id: {event_id}")
            try:
                event=Event.objects.get(id=event_id)
                print(event)
                # event_images=EventImage.objects.filter(event=event_id)
                event_serializer=EventSerializer(event,context={'request':request})
                print(event_serializer)
                # event_image_serializer=EventImageSerializer(event_images,context={"request":request},many=True)

                return Response({"event":event_serializer.data},status=status.HTTP_200_OK)
            except Event.DoesNotExist:
                return Response({"detail":'No event found'},status=404)
        else:
            one_month_ago = timezone.now() - timedelta(days=30)
            print(one_month_ago)
            event=Event.objects.filter(date__gte=one_month_ago).order_by("-created_at")[:70]
            serializer=EventSerializer(event,context={"request":request},many=True)
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
