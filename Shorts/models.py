from django.db import models
import uuid
from Accounts.models import Users
# Create your models here.

class Video(models.Model):
    id=models.UUIDField(primary_key=True, editable=False,default=uuid.uuid4)
    title=models.CharField(max_length=255)
    video=models.FileField(upload_to='Shorts')
    repost_no=models.IntegerField(default=0)
    uploader=models.ForeignKey(Users,related_name='videos',on_delete=models.CASCADE)
    Likes=models.IntegerField(default=0)
    
    def _str__(self):
        return self.id
    
class Comments(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    comment=models.TextField()
    video=models.ForeignKey(Video,related_name='Comment',on_delete=models.CASCADE)
    commenter=models.ForeignKey(Users,related_name='commenter',on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.id
    
class Like(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    liker=models.ForeignKey(Users,on_delete=models.CASCADE,related_name='Like')
    liked=models.BooleanField(default=False)
    video=models.ForeignKey(Video,related_name='liked_video',on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.id
   
