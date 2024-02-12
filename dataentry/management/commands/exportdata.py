import csv 
from django.core.management.base import BaseCommand
import datetime
from django.apps import apps
from dataentry.utils import generate_csv_file



class Command(BaseCommand):
    help = 'Export data from database to csv file'
    
    
    def add_arguments(self,parser):
        parser.add_argument('model_name',type=str,help='Model name')
        

    def handle(self, *args, **kwargs):
        model_name = kwargs['model_name'].capitalize()
        
        #search through all the installed apps for the model
        model = None
        
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label,model_name)
                break 
            except LookupError:
                pass 
        if not model:
            self.stderr.write(f'Model {model_name} couldnot found')
            return 
        
        #fetch the data from the database
        data = model.objects.all()
        
        #generate csv file path
        file_path = generate_csv_file(model_name)
        
        # open the csv file and write the data
        with open(file_path, 'w',newline='') as file:
            writer = csv.writer(file)
            
            # write the csv header
            writer.writerow([ field.name for field in model._meta.fields])
          
            
            #write data rows
            for dt in data:
                writer.writerow([getattr(dt,field.name) for field in model._meta.fields])
                
        self.stdout.write(self.style.SUCCESS('Data exported successfully!'))
        
        