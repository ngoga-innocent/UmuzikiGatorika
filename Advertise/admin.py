from django.contrib import admin
from .models import TrendingSongs,Event,EventImage
# Register your models here.
admin.site.register(TrendingSongs)
admin.site.register(Event)
admin.site.register(EventImage)