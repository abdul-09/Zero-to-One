from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
    
class InterestedTopic(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    EXPERIENCE_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('experienced', 'Experienced'),
    ]
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    experience_level = models.CharField(max_length=50, choices=EXPERIENCE_CHOICES, null=True, blank=True)
    interested_topics = models.ManyToManyField(InterestedTopic, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.full_name

class TrainingSchedule(models.Model):
    topic = models.ForeignKey(InterestedTopic, on_delete=models.CASCADE, related_name='training_schedules')
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    enrolled_users = models.ManyToManyField(User, related_name='enrolled_trainings', blank=True)

    def __str__(self):
        return self.title

    def __str__(self):
        return self.title

class Resource(models.Model):
    topic = models.ForeignKey(InterestedTopic, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField()

    def __str__(self):
        return self.title

