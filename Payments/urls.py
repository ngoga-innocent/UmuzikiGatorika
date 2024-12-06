from django.urls import path
from .views import PaymentClass
urlpatterns = [
    path('',PaymentClass.as_view(),{"action":"deposit"},name='payment'),
    path('webhook',PaymentClass.as_view(),{"action":"webhook"},name='payment'),
    
    
    # path('Gettypes/<uuid:type_id>',SongTypeClass.as_view(),name='song_type')
    # path('<uuid:copy_id>',CopiesClass.as_view(),name='copies')
]