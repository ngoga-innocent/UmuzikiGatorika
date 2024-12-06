from django.contrib import admin
from .models import Copies,SongType,SongCategory,Request
# Register your models here.

admin.site.register(Copies)
admin.site.register(SongType)
admin.site.register(SongCategory)
admin.site.register(Request)
