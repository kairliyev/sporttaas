from rest_framework import serializers, validators
from django.contrib.auth.models import User
from .models import Grouping, Membership, Coordinate
from rest_framework.validators import UniqueTogetherValidator
import re


class MemeberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Membership.objects.all(),
                fields=('user', 'grouping')
            )
        ]


class MemberListingField(serializers.RelatedField):
    def to_representation(self, value):
        return '%d: %s' % (value.pk, value.username)


class MemberField(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'first_name', 'email')


class CoordinateField(serializers.ModelSerializer):
    class Meta:
        model = Coordinate
        fields = ('latitude', 'longitude')


class GroupingSerializer(serializers.ModelSerializer):
    members = MemberListingField(many=True, read_only=True)

    class Meta:
        model = Grouping
        fields = '__all__'
        required_fields = ('title',)
        extra_kwargs = {
            'members': {'required': False},
        }

    def create(self, validated_data):
        grouping = Grouping.objects.create(**validated_data)
        Membership.objects.create(grouping=grouping, user=grouping.admin)
        return grouping

class GroupingSubSerializer(serializers.ModelSerializer):
    members = MemberListingField(many=True, read_only=True)

    class Meta:
        model = Grouping
        fields = '__all__'
        required_fields = ()
        extra_kwargs = {
            'members': {'required': False},
        }

    def update(self, instance, validated_data):
        grouping = Grouping.objects.create(**validated_data)
        Membership.objects.create(grouping=grouping, user=grouping.admin)
        return grouping


class GroupingGetSerializer(serializers.ModelSerializer):
    members = MemberField(many=True, read_only=True)
    admin = MemberField(read_only=True)
    coordinates = CoordinateField(read_only=True)

    class Meta:
        model = Grouping
        fields = ('id', 'title', 'type', 'city', 'address', 'date', 'time', 'city', 'min_people', 'price', 'description', 'created_at', 'updated_at', 'coordinates', 'admin', 'members',)
