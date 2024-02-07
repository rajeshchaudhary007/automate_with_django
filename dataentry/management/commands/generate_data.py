import os
import csv
import random
from faker import Faker
from django.core.management.base import BaseCommand


fake = Faker()

class Command(BaseCommand):
    help = 'Generate a CSV file with dummy student data'

    def add_arguments(self, parser):
        parser.add_argument('num_students', type=int, help='Number of dummy students to generate')

    def handle(self, *args, **kwargs):
        num_students = kwargs['num_students']
        students_data = self.generate_student_data(num_students)
        data_folder = 'data'
        csv_file_path = os.path.join(data_folder,'students.csv')

        with open(csv_file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Name', 'Roll No', 'Age'])

            for student in students_data:
                csv_writer.writerow([student['name'], student['roll_no'], student['age']])

        self.stdout.write(self.style.SUCCESS(f'CSV file "{csv_file_path}" has been created successfully.'))

    def generate_student_data(self, num_students):
        students_data = []

        for _ in range(num_students):
            name = fake.name()
            roll_no = fake.unique.random_number(digits=5)
            age = random.randint(18, 25)

            students_data.append({
                'name': name,
                'roll_no': roll_no,
                'age': age,
            })

        return students_data
