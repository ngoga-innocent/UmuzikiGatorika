from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta
# Create your models here.
class Subscriptions(models.Model):
    subscription_type_choice=(
        ('by_number','Number'),
        ('by_week','Week'),
        ('by_month','Month'),
        ('Donation','Donation')
    )
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user=models.ForeignKey('Accounts.Users',on_delete=models.CASCADE,null=True)
    device=models.CharField(max_length=255,null=False)
    subscription_type=models.CharField(max_length=255,null=True,blank=True,choices=subscription_type_choice,default='Donation')
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
        ('by_month','Month'),
        ('Donation','Donation')
    )
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    payment_status=models.CharField(max_length=255,choices=payment_status_choice,null=False,default='pending')
    device_tokem=models.CharField(max_length=255)
    amount=models.IntegerField()
    paid_number=models.CharField(max_length=255,default='00000000000')
    active=models.BooleanField(default=True)
    subscription_type=models.CharField(max_length=255,null=False,choices=subscription_type_choice,default='Donation')
    transaction_kind=models.CharField(max_length=50,default='Cash In')
    reference_key=models.CharField(max_length=255)
    created_at=models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f''+self.reference_key
    def is_month_over(self):
        """
        Checks if a month has passed since the last payment for this device_tokem.
        """
        last_payment = Payment.objects.filter(
            device_tokem=self.device_tokem,
            payment_status='completed'
        ).order_by('-created_at').first()
        
        if not last_payment:
            return True  # No payments found, assume the month is over
        
        # Check if 30 days have passed since the last payment
        one_month_ago = timezone.now() - timedelta(days=30)
        return last_payment.created_at < one_month_ago    
