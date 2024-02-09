import csv
from django.db import DataError
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps

class Command(BaseCommand):
    help = 'Import data from CSV File'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')
        parser.add_argument('model_name', type=str, help="Name of the model")

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        model_name = kwargs['model_name'].capitalize()

        model = None
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label, model_name)
                break
            except LookupError:
                continue

        if not model:
            raise CommandError(f'Model "{model_name}" not found in any app')
        
        
        model_fields = [field.name for field in model._meta.fields if field.name != 'id']
        print(model_fields)

        unique_identifiers = set()

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            csv_header = reader.fieldnames
            
            if csv_header != model_fields:
                raise DataError(f'CSV file doesnot match with the {model_name} table fields')
            
            
            for row in reader:
                # Check if the record already exists based on unique identifiers
                unique_identifier = tuple(row.values())
                if unique_identifier not in unique_identifiers:
                    if not model.objects.filter(**row).exists():
                        model.objects.create(**row)
                        unique_identifiers.add(unique_identifier)
                    else:
                        self.stdout.write(self.style.WARNING(f'Data already exists for {row}'))

        self.stdout.write(self.style.SUCCESS('Data imported from CSV successfully!'))
