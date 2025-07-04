from django.urls import path
from .views import CopiesClass,SongTypeClass,SongCategoryView,Search,CreateRepertoire,RequestSongView,ShouldUpdate
urlpatterns = [
    path('',CopiesClass.as_view(),name='copies'),
    path('Gettypes/',SongTypeClass.as_view(),name='song_type'),
    path('song_category',SongCategoryView.as_view(),name='song_categories'),
    path('search_song',Search.as_view(),name="search_song"),
    path('repertoire',CreateRepertoire.as_view(),name='repertoire'),
    path('request',RequestSongView.as_view(),name='request'),
    path('check_update',ShouldUpdate.as_view())
    # path('Gettypes/<uuid:type_id>',SongTypeClass.as_view(),name='song_type')
    # path('<uuid:copy_id>',CopiesClass.as_view(),name='copies')
]