from rest_framework import serializers
from main.models import Profile, Tag, TagCategory, User, Ai, Match, Message


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "height",
            "birthday",
            "description",
            "tags",
        ]


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "category"]


class TagCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TagCategory
        fields = ["id", "name"]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "profile",
        ]


class AiSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ai
        fields = [
            "id",
            "schedule",
            "last_execution",
            "next_execution",
            "profile",
        ]


class MatchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Match
        fields = [
            "id",
            "profile_a",
            "profile_b",
            "do_match_a_b",
            "do_match_b_a",
        ]


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = [
            "id",
            "msg",
            "published",
            "deletd",
            "replied_message",
            "profile",
            "match",
        ]
