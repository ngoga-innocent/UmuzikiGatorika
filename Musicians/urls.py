from django.urls import path
from .views import MusicianView,MusicalSkills
urlpatterns = [
    path('',MusicianView.as_view(),name='musician'),
    path('musical_skills',MusicalSkills.as_view(),name='musical_skills')

   
]