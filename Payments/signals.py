from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment,Subscriptions
from Notifications.send_Push_Notification import send_push_notification
@receiver(post_save,sender=Payment)
def update_subscription(instance,sender,created,**kwargs):
    if not created:
        print("signal instance", instance.payment_status,instance.subscription_type)
        if instance.payment_status == 'completed' and instance.subscription_type !='Donation':
            try:
                find_user_subscription=Subscriptions.objects.get(device=instance.device_tokem)
                find_user_subscription.subscription_type=instance.subscription_type
                find_user_subscription.active=True
                if instance.subscription_type=='by_number':
                    copies=round(instance.amount /20)
                    find_user_subscription.amount_of_copies = find_user_subscription.amount_of_copies + copies

                    
                find_user_subscription.save()
            except Subscriptions.DoesNotExist:
                subscription=Subscriptions.objects.create(device=instance.device_tokem,subscription_type=instance.subscription_type,active=True)  
                if instance.subscription_type=='by_number':
                    copies=round(instance.amount /20)
                    subscription.amount_of_copies = subscription.amount_of_copies + copies
                    subscription.save()
        elif instance.payment_status =='successful' and instance.subscription_type =='Donation':
            try:
                token = instance.device_tokem
                if token !='Donating_Device':
                    send_push_notification(token, "Thank you for The donation", "We have received your Donation worthy May God support your Daily activities")
            except Exception as e:
                print(e)
                # logger.error(f"Failed to send notification to device {token}: {e}")
    # else:
    #     try:
    #         token = instance.device_tokem
    #         if token !='Donating_Device':
    #             send_push_notification(token, "Thank you for a donation", "We have received your Donation worthy May God support your Daily activities")
    #     except Exception as e:
    #             print(e)                    
                            
                
        
    
    