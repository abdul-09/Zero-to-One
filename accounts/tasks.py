from celery import shared_task
from django.conf import settings
from .models import User
from django.core.mail import send_mail

@shared_task
def email_users(user_ids, subject, message):
    users = User.objects.filter(id__in=user_ids)
    emails = [user.email for user in users]
    sender = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, sender, emails)

    # celery -A zero_to_one worker --loglevel=info -P solo
    # celery -A zero_to_one flower
