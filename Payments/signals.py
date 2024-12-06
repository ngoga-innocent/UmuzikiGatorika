from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment,Subscriptions
@receiver(post_save,sender=Payment)
def update_subscription(instance,sender,created,**kwargs):
    if not created:
        if instance.payment_status == 'completed' and instance.subscription_type:
            try:
                find_user_subscription=Subscriptions.objects.get(device=instance.device_tokem)
                find_user_subscription.subscription_type=instance.subscription_type
                find_user_subscription.active=True
                if instance.subscription=='by_number':
                    copies=round(instance.amount /20)
                    find_user_subscription.amount_of_copies = find_user_subscription.amount_of_copies + copies

                    
                find_user_subscription.save()
            except Subscriptions.DoesNotExist:
                subscription=Subscriptions.objects.create(device=instance.device_tokem,subscription_type=instance.subscription_type,active=True)  
                if instance.subscription_type=='by_number':
                    copies=round(instance.amount /20)
                    subscription.amount_of_copies = subscription.amount_of_copies + copies
                    subscription.save()
                
        
    
    