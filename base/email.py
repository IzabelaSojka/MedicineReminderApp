from .models import Medicine
import datetime
from django.core.mail import send_mail
from django.conf import settings

from apscheduler.schedulers.background import BackgroundScheduler

email_from = settings.EMAIL_HOST_USER

def send_email():
    now = datetime.now()
    time_2 = now.strftime('%H:%M')
    for element in Medicine:
        if element.time != '' and element.mail != '':
            if time_2 == element.time:
                subject = 'You need to take the medicine' + element.name
                send_mail(subject, element.description, email_from, [element.mail, ])

sched = BackgroundScheduler(daemon=True)
sched.add_job(send_email, 'interval', seconds=60)
sched.start()

