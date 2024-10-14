from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import User

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = "Welcome to Zero to One: Farming for the Future"
        message = (
            f"Hello {instance.full_name},\n\n"
            "Thank you for signing up for the 'Zero to One: Farming for the Future' training campaign.\n"
            "Here's an overview of the training schedule and next steps.\n\n"
            "Best regards,\nKlima360 Team"
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False,
        )
