from django.db.models.signals import post_save
from .models import Copies
from django.dispatch import receiver
from Notifications.send_Push_Notification import send_to_allDevice
@receiver(post_save, sender=Copies)
def SendNotification(sender,instance,created,**kwargs):
    if created:
        send_to_allDevice("New music Sheet Uploaded",f"check out this new song " + instance.name,{"url":"umuzikigatorika://categories"})
        # Send notification to user
        