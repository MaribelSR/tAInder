from rest_framework import serializers
from main.models import Profile, Tag, TagCategory


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = [
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
        fields = ["name", "category"]


class TagCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TagCategory
        fields = ["name"]
