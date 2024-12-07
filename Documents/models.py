from django.db import models
import uuid
from Accounts.models import Users
import os
from django.utils import timezone
# Create your models here.

class SongType(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name=models.CharField(max_length=512,null=False)
    season=models.CharField(max_length=512,null=True,default='Ibihe Bisanzwe')
    thumbnail=models.ImageField(upload_to='Song_Type',null=True)

    def __str__(self):
        return self.name
class SongCategory(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name=models.CharField(max_length=512,default='Others',unique=True)
    def __str__(self):
        return self.name
    def get_song_category(self):
        return Copies.objects.filter(id=self.id)
def song_upload_path(instance, filename):
    # Get the category name
    category_name = instance.part.name
    # Replace spaces with underscores and ensure lowercase
    category_name = category_name.replace(' ', '_').lower()
    # Generate a unique filename
    filename = f"{uuid.uuid4().hex}-{filename}"
    # Return the upload path
    return os.path.join('songs_docs', category_name,filename)
class Copies(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    composer = models.TextField()
    part = models.ForeignKey(SongCategory, null=True, on_delete=models.SET_NULL)
    uploader = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, default='')
    document = models.FileField(upload_to=song_upload_path,max_length=10000)
    category = models.ForeignKey(SongType, on_delete=models.SET_NULL, null=True, default='')
    uploaded_on = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'copies'

    def __str__(self):
        return self.name

    
class Request(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name=models.CharField(max_length=255)
    requested_on=models.DateTimeField(default=timezone.now)
    status=models.BooleanField(default=False)
    
    

