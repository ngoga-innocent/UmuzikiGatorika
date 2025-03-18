from django.urls import path
from .views import PaymentClass,CheckDevicePaid
urlpatterns = [
    path('',PaymentClass.as_view(),{"action":"deposit"},name='payment'),
    path('cashout',PaymentClass.as_view(),{"action":"cashout"},name='cashout'),
    path('webhook',PaymentClass.as_view(),{"action":"webhook"},name='payment'),
    path('checkdevicepaid/',CheckDevicePaid.as_view())
    
    # path('Gettypes/<uuid:type_id>',SongTypeClass.as_view(),name='song_type')
    # path('<uuid:copy_id>',CopiesClass.as_view(),name='copies')
]