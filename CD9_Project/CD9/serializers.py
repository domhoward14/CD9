from rest_framework import serializers
from models import Texts

class TextSerializer(serializers.Serializer):
    number = serializers.IntegerField()
    date = serializers.DateTimeField()

    def create(self, validated_data):
        return Texts.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.number = validated_data.get('number', instance.number)
        instance.date = validated_data.get('date', instance.date)
        instance.save()
        return instance