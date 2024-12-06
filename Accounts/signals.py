from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Users
from Notifications.models import NotificationModal
@receiver(post_save,sender=Users)
def Notify_user(instance,sender,created,**kwargs):
    if created:
        NotificationModal.objects.create(
            type='User_Notification',
            notification=f"Welcome new user {instance.username}!",
            notification_owner=instance,
            read=False
        )
    else:
        NotificationModal.objects.create(
            type='User_Notification',
            notification=f"{instance.username} Your Account has been updated!!",
            notification_owner=instance,
            read=False
        )
