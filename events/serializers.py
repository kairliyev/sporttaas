from django.contrib.auth.models import User
from rest_framework import serializers
from events.models import Events


class EventUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username", "email", "date_joined")


class EventSerializer(serializers.ModelSerializer):
    user = EventUserSerializer(read_only=True)

    class Meta:
        model = Events
        fields = ("user", "name", "date_created")
