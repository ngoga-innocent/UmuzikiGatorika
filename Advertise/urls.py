from django.urls import path
from .views import Adverts,Trending
urlpatterns = [
    path('',Adverts.as_view(),name='advert'),
    path('trendings',Trending.as_view(),name='trending')
    
    
]
