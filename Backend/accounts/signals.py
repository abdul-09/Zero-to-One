from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import User

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Welcome to Zero-to-One Farming!',
            'Thank you for signing up. We are excited to have you on board.',
            'no-reply@zero-to-one-farming.com',
            [instance.email],
        )
