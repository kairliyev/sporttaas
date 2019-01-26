from rest_framework import serializers, validators
from django.contrib.auth.models import User
from .models import Grouping, Membership
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
        fields = ('pk', 'username', 'email')


# class AmiyanField(serializers.ModelSerializer):
#     class Meta:
#         model = Amiyan
#         fields = '__all__'



# class GroupingListSerializer(serializers.ListSerializer):
#     def update(self, instance, validated_data):
#         # Maps for id->instance and id->data item.
#         grouping_mapping = {grouping.id: grouping for grouping in instance}
#         data_mapping = {item['id']: item for item in validated_data[]}

#         # Perform creations and updates.
#         ret = []
#         for grouping_id, data in data_mapping.items():
#             grouping = grouping_mapping.get(grouping_id, None)
#             if grouping is None:
#                 ret.append(self.child.create(data))
#             else:
#                 ret.append(self.child.update(grouping, data))



class GroupingSerializer(serializers.ModelSerializer):
    members = MemberListingField(many=True, read_only=True)

    class Meta:
        model = Grouping
        fields = '__all__'
        required_fields = ('title',)
        extra_kwargs = {
            'members': {'required': False},
        }

        def validate_title(self, value):
            all_title = Grouping.objects.filter(title=value)

        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Grouping.objects.all(),
        #         fields=('members', 'title')
        #     )
        # ]

    def create(self, validated_data):
        # members_data = self.context
        # g = Grouping(**validated_data)
        # print(g)
        # for member in members_data:
        #     m = User.objects.get(pk = member)
        #     member = Membership.objects.create(grouping = g, **m)
        # validated_data["members"] = members_data
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
        # members_data = self.context
        # g = Grouping(**validated_data)
        # print(g)
        # for member in members_data:
        #     m = User.objects.get(pk = member)
        #     member = Membership.objects.create(grouping = g, **m)
        # validated_data["members"] = members_data
        grouping = Grouping.objects.create(**validated_data)
        Membership.objects.create(grouping=grouping, user=grouping.admin)
        return grouping


class GroupingGetSerializer(serializers.ModelSerializer):
    members = MemberField(many=True, read_only=True)
    admin = MemberField(read_only=True)
    # amiyan = serializers.SerializerMethodField()

    class Meta:
        model = Grouping
        fields = ('id', 'title', 'type', 'city', 'address', 'date', 'time', 'city', 'min_people', 'price', 'description', 'created_at', 'updated_at', 'admin', 'members',)

    # def get_amiyan(self, obj):
    #     a = AmiyanField(data=Amiyan.objects.filter(group=obj.pk), many=True)
    #     if a.is_valid():
    #         return a.errors
    #     return a.data