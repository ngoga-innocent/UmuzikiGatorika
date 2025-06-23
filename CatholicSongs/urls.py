
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache

import os
urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('',include('Home.urls')),
    path('account/',include('Accounts.urls'),name='account'),
    path('documents/',include('Documents.urls'),name='documents'),
    path('musician/',include('Musicians.urls'),name='musician'),
    path('advertise/',include('Advertise.urls'),name='advertise'),
    path('notification/',include('Notifications.urls'),name='notification'),
    path('shorts/',include('Shorts.urls'),name='shorts'),
    path('payments/',include('Payments.urls'),name='payments'),
    path('staff/',include('Staff.urls'),name='staff'),
]
# urlpatterns += static('/.well-known/', document_root=os.path.join(settings.BASE_DIR, 'static/.well-known'))
urlpatterns += [
    path(
        '.well-known/assetlinks.json',
        never_cache(TemplateView.as_view(
            template_name='.well-known/assetlinks.json',
            content_type='application/json'
        )),
        name='assetlinks'
    )
]
urlpatterns += [
    path(
        '.well-known/apple-app-site-association',
        never_cache(TemplateView.as_view(
            template_name='.well-known/apple-app-site-association',
            content_type='application/json'
        )),
        name='apple-app-site-association'
    )
]
# urlpatterns += static('/.well-kno file?wn/apple-app-site-association.json', document_root=os.path.join(settings.BASE_DIR, 'static/.well-known'))

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)