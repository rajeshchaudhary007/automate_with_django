from django.contrib import admin
from .models import List,Subscriber,Email,Sent


# Register your models here.

admin.site.register(List)
admin.site.register(Subscriber)
admin.site.register(Email)
admin.site.register(Sent)