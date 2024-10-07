# Generated by Django 4.2.14 on 2024-10-07 08:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('start_time', models.DateTimeField()),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='training_schedules', to='accounts.interestedtopic')),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('link', models.URLField()),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resources', to='accounts.interestedtopic')),
            ],
        ),
    ]
