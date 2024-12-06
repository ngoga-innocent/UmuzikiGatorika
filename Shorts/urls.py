from django.urls import path
from .views import ShortsView,LikeView,CommentView
urlpatterns = [
    path('',ShortsView.as_view(),name='shorts'),
    path('like',LikeView.as_view(),name='shorts'),
    path('comment',CommentView.as_view(),name='shorts'),
    

   
]