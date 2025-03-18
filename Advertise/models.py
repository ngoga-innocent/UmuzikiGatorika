from django.db import models
import uuid
from Accounts.models import Users
from django.utils import timezone
# Create your models here.
class Event(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    title=models.CharField(max_length=255)
    description=models.TextField()
    thumbnail=models.ImageField(upload_to='Ads_Adv')
    location=models.CharField(max_length=255,default="")
    date=models.DateTimeField(default=timezone.now)
    created_at=models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.title
    
class EventImage(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    images=models.ImageField(upload_to='Event Profile')
class TrendingSongs(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    # thumbnail=models.ImageField(upload_to='Trending_Songs')
    link=models.CharField(max_length=255)
    created_at=models.DateTimeField(default=timezone.now)
class Comments(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    event=models.ForeignKey(Event,on_delete=models.CASCADE,related_name='event_comments')
    user=models.ForeignKey(Users,on_delete=models.CASCADE,related_name='user_comments',null=True,blank=True)
    comment=models.TextField()
    created_at=models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.comment[0:10]
    class Meta:
        ordering=['-created_at']
        verbose_name_plural='Comments'
class Likes(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    event=models.ForeignKey(Event,on_delete=models.CASCADE,related_name='event_like')
    device=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.device
    
    

