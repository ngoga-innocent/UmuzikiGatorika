from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import Staff,MusicSheetView,SongCategoryView,MusicianView,TredingVideo,EventsView,NotificationView,Requests,Payments

urlpatterns = [
    path('',Staff.as_view(),name='dashboard'),
    path('music_sheets',MusicSheetView.as_view(),name='music_sheets'),
    path('music_sheets/<uuid:name>',MusicSheetView.as_view(),name='single_sheet'),
    path('song_category',SongCategoryView.as_view(),name='song_category'),
    path('category/delete/',SongCategoryView.as_view(),name='song_category_delete'),
    path('musicians',MusicianView.as_view(),name='musicians'),
    path('tredings',TredingVideo.as_view(),name='tredings'),
    path('events',EventsView.as_view(),name='events'),
    path('notifications',NotificationView.as_view(),name='notifications'),
    path('requests',Requests.as_view(),name='requests'),
    path('payments',Payments.as_view(),name='web_payments'),
    # path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    # path('webhook',PaymentClass.as_view(),{"action":"webhook"},name='payment'),
    # path('webhook', PaymentClass.as_view(),{"action":"webhook"},name='payment'
    # path('webhook',PaymentClass.as_view(),{"action":"webhook"},name='payment'),
    
    
    
    # path('Gettypes/<uuid:type_id>',SongTypeClass.as_view(),name='song_type')
    # path('<uuid:copy_id>',CopiesClass.as_view(),name='copies')
]
