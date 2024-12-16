from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import NotificationModal
from .serializers import NotificationSeriazer,DeviceSerializer
from django.db.models import Q
from rest_framework import status
from django.db.utils import IntegrityError
from .models import Device
from .send_Push_Notification import send_email
from django.conf import settings
# Create your views here.

class NotificationView(APIView):
    def get(self,request):
        if request.user.is_authenticated:
            notifications=NotificationModal.objects.filter(Q(notification_owner=request.user) | Q(type='App_Notificaion')).order_by('-created_at')
            seriazer=NotificationSeriazer(notifications,many=True)
            return Response({"notifications":seriazer.data},status=200)
        notifications=NotificationModal.objects.filter(type='App_Notificaion').order_by('-created_at')
        seriazer=NotificationSeriazer(notifications,many=True)
        return Response({"notifications":seriazer.data},status=200)
    def put(self,request,pk):
        try:
            notification=NotificationModal.objects.get(pk=pk)

        except NotificationModal.DoesNotExist:
            return Response({"details":"provided notfication Does not exists"},status=404)
        serializer=NotificationSeriazer(notification,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"details":"notification updated successfull"},status=200)
        else:
            return Response({"errors":serializer.errors},status=401)
        
    def delete(self,request,pk):
        try:
            notification=NotificationModal.objects.get(pk=pk)
            notification.delete()
            return Response({"details":"Notification deleted Successfully"})
        except NotificationModal.DoesNotExist:
            return Response({"error":"provided notification does not exist"},status=404)
class RegisterDevice(APIView):
    def post(self, request):
        token = request.data.get('token')

        if not token:
            return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            device, created = Device.objects.get_or_create(token=token)
            if created:
                return Response({"message": "Device registered successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Device already registered"}, status=status.HTTP_200_OK)
        except IntegrityError:
            return Response({"error": "Device token must be unique"}, status=status.HTTP_400_BAD_REQUEST)
        
class SendEmail(APIView):
    def post(self, request):
        email = request.data.get('email')
        subject = request.data.get('subject')
        message = request.data.get('message')

        if not email or not subject or not message:
            return Response({"error": "Email, subject, and message are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            send_email(subject, message, [settings.EMAIL_HOST_USER])
            return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Failed to send email: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        


