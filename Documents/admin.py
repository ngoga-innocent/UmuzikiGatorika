from django.contrib import admin
from .models import Copies,SongType,SongCategory,Request,AppVersion
# Register your models here.

admin.site.register(Copies)
admin.site.register(SongType)
admin.site.register(SongCategory)
admin.site.register(Request)
admin.site.register(AppVersion)