from rest_framework import serializers
from models import Texts,UserProfile, App_list, Phone_Calls, Photo_Messages, Web_History


class TextSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Texts
        fields = ('number', 'date', 'content', 'owner', 'pk')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('user', 'email', 'fb_token')

class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App_list
        fields = ('appName', 'installDate')

class PhoneCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone_Calls
        fields = ('number', 'convoTime', 'date')

class PhotoMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_Messages
        fields = ('number', 'date')

class WebHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Web_History
        fields = ('site', 'rating', 'date')


