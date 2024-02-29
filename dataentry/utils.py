import csv
import datetime
import time
import hashlib
import os
from django.apps import apps
from django.core.management.base import CommandError
from django.db import DataError
from django.core.mail import EmailMessage
from django.conf import settings
import datetime

from emails.models import Email, Sent,EmailTracking,Subscriber

def get_all_custom_models():
    default_models = ['ContentType', 'Session','LogEntry', 'Group','Permission','User','Uploads']
    
    #try to get all the apps
    custom_models = []
    
    for model in apps.get_models():
        if model.__name__ not in default_models:
            custom_models.append(model.__name__)
    return custom_models



def check_csv_errors(file_path,model_name):
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
    
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            csv_header = reader.fieldnames
            
            if csv_header != model_fields:
                raise DataError(f'CSV file doesnot match with the {model_name} table fields')
            
    except Exception as e:
        raise e
    
    return model

def send_email_notification(mail_subject,message,to_email,attachment=None,email_id=None):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        for recepient_email in to_email:
            #create EmailTracking record
            if email_id:
                email = Email.objects.get(pk=email_id)
                subscriber = Subscriber.objects.get(email_list=email.email_list,email_address=recepient_email)
                timestamp = str(time.time())
                data_to_hash = f"{recepient_email}{timestamp}"
                unique_id = hashlib.sha256(data_to_hash.encode()).hexdigest
                email_tracking = EmailTracking.objects.create(
                    email = email,
                    subscriber = subscriber,
                    unique_id = unique_id,
            )
            
            #Generate the tracking pixel
            click_tracking_url = f"http:127.0.0.1:8000/emails/track/click/{unique_id}"
            
            # Search for the links in email body
            
            
            # if there are links or urls in the email body, inject our click tracking url to that original link
            
            mail = EmailMessage(mail_subject,message,from_email,to=to_email)
            if attachment is not None:
                mail.attach_file(attachment)
                
            mail.content_subtype = "html"
            mail.send()
        
        #store the total sent email inside the Sent Model
        if email:
            sent = Sent()
            sent.email = email
            sent.total_sent = email.email_list.count_emails()
            sent.save()
        
    except Exception as e:
        raise e
    
    
def generate_csv_file(model_name):
    #generate the timestamp of current date and time
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    
    #define the csv file name/path
    export_dir = 'exported_data'
    
    file_name = f'exported_{model_name}_data_{timestamp}.csv'
    file_path = os.path.join(settings.MEDIA_ROOT,export_dir,file_name)
    return file_path
    
    