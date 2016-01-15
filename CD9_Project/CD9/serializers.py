from rest_framework import serializers
from models import Texts,UserProfile

class TextSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Texts
        fields = ('number', 'date', 'content', 'owner')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('user', 'email', 'fb_token')