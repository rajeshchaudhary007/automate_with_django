
from django.contrib import admin
from django.urls import path,include

from django.conf.urls.static import static
from django.conf import settings

from .views import home,celery_test,register,login_view,logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('dataentry/',include('dataentry.urls')),
    path('celery-test/',celery_test),
    path('register/',register,name='register'),
    path('login/',login_view, name ='login'),
    path('logout/',logout,name='logout'),
    path('emails/',include('emails.urls')),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)