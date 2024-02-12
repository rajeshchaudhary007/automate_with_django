from django.shortcuts import render,redirect
from django.contrib import messages

from django.conf import settings

from emails.models import Subscriber
from emails.tasks import send_email_task
from .forms import EmailForm
from dataentry.utils import send_email_notification

# Create your views here.

def send_email(request):
    if request.method == 'POST':
        email_form = EmailForm(request.POST, request.FILES)
        if email_form.is_valid():
            email = email_form.save()
            
            #send an email
            mail_subject = request.POST.get('subject')
            message = request.POST.get('body')
            email_list = request.POST.get('email_list')
            
            #access the selected email list
            email_list = email.email_list
            
            subscribers = Subscriber.objects.filter(email_list=email_list)
            
            to_email = [email.email_address for email in subscribers ]
            
            if email.attachment:
                attachment = email.attachment.path
            else:
                attachment = None
            
            #hand over email task to celery
            send_email_task.delay(mail_subject,message,to_email,attachment)

            
         
            
            messages.success(request,'Email sent successfully!')
            return redirect('send_email')
    else:
        email_form = EmailForm()
    
    context = {'email_form':email_form}
    return render(request, 'emails/send-email.html',context)