from rest_framework import serializers
from .models import User, InterestedTopic
from django.contrib.auth.password_validation import validate_password

class InterestedTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestedTopic
        fields = ['id', 'name']


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestedTopic
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    interested_topics = TopicSerializer(many=True, read_only=True)

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
