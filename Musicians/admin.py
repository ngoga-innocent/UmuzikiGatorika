from django.contrib import admin
from .models import MusicianModel,MusicSkillChoices
# Register your models here.
admin.site.register(MusicianModel)
admin.site.register(MusicSkillChoices)