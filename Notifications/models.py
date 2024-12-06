from django.db import models
import uuid
from Accounts.models import Users

# Create your models here.
class NotificationModal(models.Model):
    notification_choice=(
       ('App_Notificaion','App Notification'),
       ('User_Notification','User Notification')
    )
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    type=models.CharField(choices=notification_choice,default='App_Notification',max_length=255)
    notification=models.TextField()
    read=models.BooleanField(default=False)
    notification_owner=models.ForeignKey(Users,on_delete=models.CASCADE,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     ordering=['-created_at']
    # def __str__(self):
    #     return self.created_at
class Device(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    token=models.CharField(max_length=255)    

    def __str__(self):
        return self.token  