from rest_framework import serializers
from main.models import Profile, Tag, TagCategory, User, Ai, Match, Message


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "height",
            "birthday",
            "description",
            "tags",
        ]


class TagCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TagCategory
        fields = ["id", "name"]


class TagSerializer(serializers.ModelSerializer):
    category = TagCategorySerializer()

    class Meta:
        model = Tag
        fields = ["id", "name", "category"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "profile",
            "username",
            "first_name",
            "last_name",
        ]


class AiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ai
        fields = [
            "id",
            "profile",
            "username",
            "first_name",
            "last_name",
        ]


class ProfileNestedSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    user_set = UserSerializer(many=True)
    ai_set = AiSerializer(many=True)

    class Meta:
        model = Profile
        fields = "__all__"


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
