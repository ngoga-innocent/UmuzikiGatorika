from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Event
from Notifications.models import Device
from Notifications.send_Push_Notification import send_push_notification
@receiver(post_save,sender=Event)
def send_notification(instance, sender, created, **kwargs):
    if created:
        all_devices=Device.objects.all()
        for device in all_devices:
            send_push_notification(device.token, f"New Event New Event on {instance.date}",f"{instance.title}")
