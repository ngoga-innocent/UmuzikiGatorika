from django.db import models
import uuid
from django.utils import timezone
# Create your models here.
class Subscriptions(models.Model):
    subscription_type_choice=(
        ('by_number','Number'),
        ('by_week','Week'),
        ('by_month','Month')
    )
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user=models.ForeignKey('Accounts.Users',on_delete=models.CASCADE,null=True)
    device=models.CharField(max_length=255,null=False)
    subscription_type=models.CharField(max_length=255,null=False,choices=subscription_type_choice)
    amount_of_copies=models.IntegerField(null=True,default=0)
    active=models.BooleanField(default=False)
    created_at=models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f''+ self.subscription_type
class Payment(models.Model):
    payment_status_choice=(
        ('completed','completed'),
        ('pending','pending'),
        ('failed','failed')
    )
    subscription_type_choice=(
        ('by_number','Number'),
        ('by_week','Week'),
        ('by_month','Month')
    )
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    payment_status=models.CharField(max_length=255,choices=payment_status_choice,null=False,default='pending')
    device_tokem=models.CharField(max_length=255)
    amount=models.IntegerField()
    active=models.BooleanField(default=True)
    subscription_type=models.CharField(max_length=255,null=False,choices=subscription_type_choice)
    reference_key=models.CharField(max_length=255)
    created_at=models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f''+self.reference_key    
