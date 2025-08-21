from rest_framework import serializers
from main.models import Profile, Tag, TagCategory, User, Ai, Match, Message


class ProfileSerializer(serializers.ModelSerializer):
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


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "category"]


class TagCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TagCategory
        fields = ["id", "name"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "profile",
        ]


class AiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ai
        fields = [
            "id",
            "last_execution",
            "profile",
        ]


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = [
            "id",
            "ai_profile",
            "user_profile",
            "do_match",
            "summary",
        ]


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            "id",
            "msg",
            "published",
            "deleted",
            "replied_message",
            "profile",
            "match",
            "summarized",
        ]
