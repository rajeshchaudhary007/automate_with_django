from django.contrib import admin

# Register your models here.
from .models import Stock,StockData

class StockAdmin(admin.ModelAdmin):
    search_fields = ('id','name','symbol')

admin.site.register(Stock,StockAdmin)
admin.site.register(StockData)