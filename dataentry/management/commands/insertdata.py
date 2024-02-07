from django.core.management.base import BaseCommand
from dataentry.models import Student

class Command(BaseCommand):
    help = 'It will insert data to the database'
    
    
    def handle(self, *args, **kwargs):
        
        datasets = [
            {'roll_no':102,'name':'Miller','age':22},
            {'roll_no':103,'name':'Mike','age':21},
            {'roll_no':104,'name':'Joya','age':20},
            {'roll_no':105,'name':'Ele','age':19},
            {'roll_no':106,'name':'Mitchel','age':22},
            {'roll_no':107,'name':'Givan','age':21},
            {'roll_no':108,'name':'Jerry','age':20},
            {'roll_no':109,'name':'Illeana','age':19},
        ]
        
        
        
        for data in datasets:
            roll_no = data['roll_no']
            existing_record = Student.objects.filter(roll_no=roll_no).exists()
            
            if not existing_record:
                Student.objects.create(roll_no=data['roll_no'],name=data['name'],age=data['age'])
            else:
                self.stdout.write(self.style.WARNING(f'Student with roll no {roll_no} already exists'))
        
        self.stdout.write(self.style.SUCCESS('Data inserted successfully!'))