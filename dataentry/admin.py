from django.contrib import admin
from .models import Student,Customer

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_no', 'age')

admin.site.register(Student, StudentAdmin)
admin.site.register(Customer)