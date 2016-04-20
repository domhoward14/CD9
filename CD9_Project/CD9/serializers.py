from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from models import *
from django.contrib.auth.models import User
from rest_framework_bulk import (
    BulkListSerializer,
    BulkSerializerMixin,
    ListBulkCreateUpdateDestroyAPIView,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Texts
        fields = ('number', 'date', 'content', 'pk','text_type')

class PingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pings
        fields = ('hit', 'time',)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('user', 'email', 'fb_token', 'auth_code', 'id', 'gcm_reg_id' )

class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App_list
        fields = ('appName', 'installDate', 'packageName', 'contentRating', 'siteLink', 'marketUrl', "description")

class PhoneCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone_Calls
        fields = ('number', 'convoTime', 'date', 'call_type')

class PhotoMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo_Messages
        fields = ('number', 'date')

class WebHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Web_History
        fields = ('site','installDate')
