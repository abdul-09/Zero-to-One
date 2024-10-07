from rest_framework import serializers
from .models import User, InterestedTopic, Resource, TrainingSchedule
from django.contrib.auth.password_validation import validate_password

class InterestedTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestedTopic
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    interested_topics = InterestedTopicSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'phone_number', 'location', 'experience_level', 'interested_topics']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    interested_topics = serializers.PrimaryKeyRelatedField(queryset=InterestedTopic.objects.all(), many=True)

    class Meta:
        model = User
        fields = ['email', 'full_name', 'phone_number', 'location', 'experience_level', 'interested_topics', 'password', 'confirm_password',]

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        interested_topics = validated_data.pop('interested_topics')
        user = User.objects.create_user(**validated_data)
        user.interested_topics.set(interested_topics)
        user.save()
        return user

class TrainingScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingSchedule
        fields = ['id', 'title', 'description', 'start_time']

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'title', 'description', 'link']

class UserDashboardSerializer(serializers.ModelSerializer):
    enrolled_topics = InterestedTopicSerializer(source='interested_topics', many=True)
    available_topics = serializers.SerializerMethodField()
    resources = serializers.SerializerMethodField()
    training_schedules = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'full_name', 'email', 'location', 'experience_level',
            'enrolled_topics', 'available_topics', 'resources', 'training_schedules'
        ]

    def get_available_topics(self, obj):
        """Retrieve topics the user has not enrolled in."""
        enrolled_topic_ids = obj.interested_topics.values_list('id', flat=True)
        available_topics = InterestedTopic.objects.exclude(id__in=enrolled_topic_ids)
        return InterestedTopicSerializer(available_topics, many=True).data

    def get_resources(self, obj):
        """Retrieve resources for enrolled topics."""
        resources = Resource.objects.filter(topic__in=obj.interested_topics.all())
        return ResourceSerializer(resources, many=True).data

    def get_training_schedules(self, obj):
        """Retrieve training schedules for enrolled topics."""
        schedules = TrainingSchedule.objects.filter(topic__in=obj.interested_topics.all())
        return TrainingScheduleSerializer(schedules, many=True).data