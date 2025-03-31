from django.contrib import admin
from .models import Payment, Subscriptions

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'device_tokem', 'payment_status', 'amount', 'created_at')
    search_fields = ('device_tokem', 'payment_status','paid_number')  # Enables search by these fields
    list_filter = ('payment_status', 'created_at','paid_number')  # Adds filter options in admin

# @admin.register(Subscriptions)
# class SubscriptionsAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'plan', 'start_date', 'end_date', 'status')
#     search_fields = ('user__username', 'plan', 'status')  # Search by user and plan
#     list_filter = ('status', 'start_date', 'end_date')  # Filter options

