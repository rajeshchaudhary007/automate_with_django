
from django.contrib import admin
from django.urls import path,include
from .views import home,celery_test
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('dataentry/',include('dataentry.urls')),
    path('celery-test/',celery_test),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)