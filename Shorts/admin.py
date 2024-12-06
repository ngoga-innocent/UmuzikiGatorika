from django.contrib import admin
from .models import Like,Comments,Video
# Register your models here.
admin.site.register(Video)
admin.site.register(Like)
admin.site.register(Comments)