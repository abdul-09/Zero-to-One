# Generated by Django 4.2.14 on 2024-10-16 14:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_experience_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainingschedule',
            name='enrolled_users',
            field=models.ManyToManyField(blank=True, related_name='enrolled_trainings', to=settings.AUTH_USER_MODEL),
        ),
    ]
