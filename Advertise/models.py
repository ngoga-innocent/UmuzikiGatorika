from django.db import models
import uuid
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

