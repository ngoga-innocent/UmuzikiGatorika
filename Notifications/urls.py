from django.urls import path
from .views import NotificationView,RegisterDevice,SendEmail,AppAnnouncementView,ChatNotification
urlpatterns = [
    path('',NotificationView.as_view(),name='notification'),
    path('<uuid:pk>',NotificationView.as_view(),name='notification_update'),
    path('register_device',RegisterDevice.as_view()),
    path('send_email',SendEmail.as_view()),
    path('app-announcements/',AppAnnouncementView.as_view(),name='app-announcements'),
    path('chat-notofication/',ChatNotification.as_view(),name='chat-notification'),
    # path('Gettypes/<uuid:type_id>',SongTypeClass.as_view(),name='song_type')
    # path('<uuid:copy_id>',CopiesClass.as_view(),name='copies')
]