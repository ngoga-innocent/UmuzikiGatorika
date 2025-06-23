from django.urls import path
from .views import HomeView,Home,AboutView,apple_app_site_association

urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('privacy',HomeView,name='privacy'),
    path('about_us', AboutView, name='about_us')
    
    
]
urlpatterns += [
    path('.well-known/apple-app-site-association', apple_app_site_association)
]
