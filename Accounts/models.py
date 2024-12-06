from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.

class Users(AbstractUser):
    
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    musician=models.BooleanField(default=False)
    phone_number=models.CharField(max_length=16,null=True,blank=True,unique=True)
    profile=models.ImageField(upload_to='Profile',null=True,blank=True)
    
    REQUIRED_FIELDS=[]
    