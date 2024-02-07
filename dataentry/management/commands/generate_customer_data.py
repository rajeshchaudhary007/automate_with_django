import csv
import os
from django.core.management.base import BaseCommand
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Generate a CSV file with dummy customer data'

    def add_arguments(self, parser):
        parser.add_argument('num_customers', type=int, help='Number of dummy customers to generate')

    def handle(self, *args, **kwargs):
        num_customers = kwargs['num_customers']
        customers_data = self.generate_customer_data(num_customers)
        data_folder = 'data'
        os.makedirs(data_folder, exist_ok=True)
        csv_file_path = os.path.join(data_folder, 'customers.csv')

        with open(csv_file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['customer_name', 'country'])

            for customer in customers_data:
                csv_writer.writerow([customer['customer_name'], customer['country']])

        self.stdout.write(self.style.SUCCESS(f'CSV file "{csv_file_path}" has been created successfully.'))

    def generate_customer_data(self, num_customers):
        customers_data = []

        for _ in range(num_customers):
            customer_name = fake.company()
            country = fake.country()

            customers_data.append({
                'customer_name': customer_name,
                'country': country,
            })

        return customers_data
