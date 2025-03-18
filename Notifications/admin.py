from django.contrib import admin
from .models import NotificationModal,Device,AppAnnouncement
# Register your models here.
admin.site.register(NotificationModal)
admin.site.register(Device)
@admin.register(AppAnnouncement)
class AppAnnouncementAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "is_active", "timestamp")
    list_filter=("timestamp",)