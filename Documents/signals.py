from django.db.models.signals import post_save
from .models import Copies,Request
from django.dispatch import receiver
from Notifications.send_Push_Notification import send_to_allDevice
@receiver(post_save, sender=Copies)
def SendNotification(sender,instance,created,**kwargs):
    if created:
        pass
        # send_to_allDevice("New music Sheet Uploaded",f"check out this new song " + instance.name,{"url":"umuzikigatorika://categories"})
    else:
        if instance.checked:
            send_to_allDevice("Indirimbo nshya ishyizwe kuri application",f"Ntucikwe n'iyi ndirimbo " + instance.name + " Ubu mushobora kuyidownloadinga",{"url":"umuzikigatorika://categories"})
        # Send notification to user
@receiver(post_save,sender=Request)
def SendRequestNotification(sender,instance,created,**kwargs):
    if created:
        send_to_allDevice("Gusaba Indirimbo",f"Hari umukristu ucyeneye " + instance.name + f" yishyire kuri application Nimba uyifite",{"url":"umuzikigatorika://requests"})
        # Send notification to user        