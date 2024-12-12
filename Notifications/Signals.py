from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import NotificationModal, Device
from .send_Push_Notification import send_push_notification
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=NotificationModal)
def created_notification(sender, instance, created, **kwargs):
    print(instance.type)
    if created:
        try:
            if instance.type == 'App_Notificaion':
                devices = Device.objects.all()
                for device in devices:
                    if device.token:  # Ensure the device has a valid token
                        try:
                            send_push_notification(device.token, "New Notification", f"{instance.notification}",{"url":"umuzikigatorika://notifications"})
                        except Exception as e:
                            print(e)
                            logger.error(f"Failed to send notification to device {device.id}: {e}")
        except Exception as e:
            print("error sending notification",e)
            logger.error(f"Error in NotificationModal post_save signal: {e}")
