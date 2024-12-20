from django.db.models.signals import post_save
from .models import Copies,Request
from django.dispatch import receiver
from Notifications.send_Push_Notification import send_to_allDevice
@receiver(post_save, sender=Copies)
def SendNotification(sender,instance,created,**kwargs):
    if created:
        send_to_allDevice("New music Sheet Uploaded",f"check out this new song " + instance.name,{"url":"umuzikigatorika://categories"})
    else:
        if instance.checked:
            send_to_allDevice("Music Sheet Approved",f"Don't Miss this new song " + instance.name + " Is now Available to be  Downloaded",{"url":"umuzikigatorika://categories"})
        # Send notification to user
@receiver(post_save,sender=Request)
def SendRequestNotification(sender,instance,created,**kwargs):
    if created:
        send_to_allDevice("New Request",f"A new request has been made" + instance.name,{"url":"umuzikigatorika://requests"})
        # Send notification to user        