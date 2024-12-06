from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import NotificationModal,Device
from .send_Push_Notification import send_push_notification

@receiver(post_save,sender=NotificationModal)
def created_notification(instance,sender,created,**kwargs):
    if created:
        if instance.type == 'App Notification':
            devices=Device.objects.all()
            for device in devices:
                send_push_notification(device.token, "Notification" ,f"{instance.notification}")
            
        