from django.urls import path
from .views import HomeView,Home,AboutView
urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('privacy',HomeView,name='privacy'),
    path('about_us', AboutView, name='about_us')
    
    
]
