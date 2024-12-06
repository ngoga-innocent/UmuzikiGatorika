from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MusicianModel
from Accounts.models import Users
@receiver(post_save,sender=MusicianModel)
def change_user_musician(instance,sender,created,**kwargs):
    if created:
        obj=Users.objects.get(pk=instance.user.id)
        obj.musician=True
        obj.save()