from django.urls import path
from .views import Adverts,Trending,CommentView,LikeView
urlpatterns = [
    path('',Adverts.as_view(),name='advert'),
    path('trendings',Trending.as_view(),name='trending'),
    path('comments/', CommentView.as_view(), name='comment'),
    path('likes',LikeView.as_view(),name='like')
    
    
]
