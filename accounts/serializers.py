from rest_framework import serializers
from .models import User, InterestedTopic, Resource, TrainingSchedule
from django.contrib.auth.password_validation import validate_password
from drf_recaptcha.fields import ReCaptchaV2Field


class InterestedTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestedTopic
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    interested_topics = InterestedTopicSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'phone_number', 'location', 'experience_level', 'interested_topics']

class RegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    # captcha = ReCaptchaV2Field()

    class Meta:
        model = User
        fields = ['full_name', 'email', 'password', 'confirm_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove confirm_password from the validated_data
        # validated_data.pop('captcha')
        user = User.objects.create_user(**validated_data)
        return user

class ProfileUpdateSerializer(serializers.ModelSerializer):
    interested_topics = serializers.PrimaryKeyRelatedField(queryset=InterestedTopic.objects.all(), many=True)

    class Meta:
        model = User
        fields = ['phone_number', 'location', 'experience_level', 'interested_topics']

    def update(self, instance, validated_data):
        interested_topics = validated_data.pop('interested_topics', None)
        instance = super().update(instance, validated_data)
        if interested_topics:
            instance.interested_topics.set(interested_topics)
        return instance

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'title', 'description', 'link']

class TrainingScheduleSerializer(serializers.ModelSerializer):
    topic = serializers.SerializerMethodField()

    class Meta:
        model = TrainingSchedule
        fields = ['id', 'topic', 'title', 'description', 'start_time']

    def get_topic(self, obj):
        # Return the topic's name instead of the FK ID
        return obj.topic.name


class UserDashboardSerializer(serializers.ModelSerializer):
    interested_topics = InterestedTopicSerializer(many=True)
    available_trainings = serializers.SerializerMethodField()
    resources = serializers.SerializerMethodField()
    training_schedules = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'full_name', 'email', 'location', 'experience_level', 
            'interested_topics', 'enrolled_trainings', 
            'available_trainings', 'resources', 'training_schedules'
        ]

    def get_available_trainings(self, obj):
        # Fetch the trainings that the user is not enrolled in
        enrolled_training_ids = obj.enrolled_trainings.values_list('id', flat=True)
        available_trainings = TrainingSchedule.objects.exclude(id__in=enrolled_training_ids)
        return TrainingScheduleSerializer(available_trainings, many=True).data

    def get_resources(self, obj):
        # Fetch topics related to the user's enrolled trainings
        enrolled_topics = obj.enrolled_trainings.values_list('topic', flat=True).distinct()
        
        # Retrieve resources related to those topics
        resources = Resource.objects.filter(topic__in=enrolled_topics)
        return ResourceSerializer(resources, many=True).data
    
    def get_training_schedules(self, obj):
        # Get training schedules based on user's interested topics
        schedules = TrainingSchedule.objects.filter(topic__in=obj.interested_topics.all())
        return TrainingScheduleSerializer(schedules, many=True).data
