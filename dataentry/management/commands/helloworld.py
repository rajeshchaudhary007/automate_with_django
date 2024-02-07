from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "prints hello world"
    
    
    def handle(self,*args, **kwargs):
        self.stdout.write("Hello World")
        