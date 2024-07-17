from rest_framework import serializers
from .models import URLAnalysis, Feedback
from django.contrib.auth.models import User
from .models import MLModel

class URLAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = URLAnalysis
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['analysis', 'is_correct', 'user', 'created_at']

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class ModelDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLModel
        fields = ('url', 'prediction', 'analyzed_at')