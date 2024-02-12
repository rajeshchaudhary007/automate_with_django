from config.celery import app
from dataentry.utils import send_email_notification


@app.task
def send_email_task(mail_subject,message,to_email,attachment):
    # try:
        send_email_notification(mail_subject,message,to_email,attachment)
        return 'Email sending task executed successfully.'